from rest_framework import serializers
from apps.finance.models import Transaction
from django.utils import timezone

class TransactionSerializer(serializers.ModelSerializer):
    # Borramos la línea de 'user = ...' que tenías aquí arriba ❌
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'category', 'category_name', 
            'amount', 'description', 'type', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value

    def validate_date(self, value):
        now = timezone.now()
        # Si 'value' es Date (solo fecha), comparamos con .now().date()
        if value.date() > now.date() + timezone.timedelta(days=365):
            raise serializers.ValidationError("La fecha es demasiado lejana en el futuro.")
        return value