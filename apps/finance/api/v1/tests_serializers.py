from rest_framework import serializers
from apps.finance.models import Category, Transaction, Budget
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone

class CategorySerializerTest(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'is_default', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['user', 'name'],
                message="Ya tienes una categoría con este nombre."
            )
        ]
        
    def validate_name(self, value):

        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre de la categoría es demasiado corto.")
        return value.strip()

    def validate_icon(self, value):

        if len(value) > 50:
            raise serializers.ValidationError(
                f"El nombre del icono es demasiado largo ({len(value)}/50). "
            )
        if not value.strip():
            raise serializers.ValidationError("El icono no puede estar vacío.")
        return value

class TransactionSerializerTest(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'category', 'category_name', 'amount', 
            'description', 'type', 'date', 'created_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'user']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value

    def validate_date(self, value):

        if value > timezone.now().date() + timezone.timedelta(days=365):
            raise serializers.ValidationError("La fecha no puede ser mayor a un año en el futuro.")
        return value

class BudgetSerializerTest(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Budget
        fields = [
            'id', 'category', 'category_name', 'limit_amount', 'month', 'year', 'user'
        ]
        read_only_fields = ['id', 'user']

        validators = [
            UniqueTogetherValidator(
                queryset=Budget.objects.all(),
                fields=['user', 'category', 'month', 'year'],
                message="Ya existe un presupuesto para esta categoría en este periodo."
            )
        ]

    def validate_limit_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite del presupuesto debe ser mayor a cero.")
        return value

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("El mes debe estar entre 1 y 12.")
        return value

    def validate_year(self, value):
        current_year = timezone.now().year
        if value < current_year - 1 or value > current_year + 5:
            raise serializers.ValidationError(f"El año debe estar entre {current_year - 1} y {current_year + 5}.")
        return value