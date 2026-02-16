from rest_framework import serializers
from apps.finance.models import Budget
from django.utils import timezone

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'limit_amount', 'month', 'year']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super(BudgetSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['category'].read_only = True
            self.fields['month'].read_only = True
            self.fields['year'].read_only = True

    def validate(self, data):
        # Validación de fecha pasada (Solo para nuevos registros)
        if not self.instance:
            month = data.get('month')
            year = data.get('year')
            now = timezone.now()
            if year < now.year or (year == now.year and month < now.month):
                raise serializers.ValidationError("No puedes crear presupuestos para meses pasados.")
        return data

    def validate_limit_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite debe ser mayor a cero.")
        return value

    def validate_month(self, value):
        if not (1 <= value <= 12):
            raise serializers.ValidationError("Mes inválido.")
        return value

    def validate_year(self, value):
        current_year = timezone.now().year
        if value < current_year or value > current_year + 5:
            raise serializers.ValidationError(f"Año fuera de rango.")
        return value