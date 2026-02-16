from rest_framework import serializers
from apps.finance.models import Transaction
from django.utils import timezone

class TransactionSerializer(serializers.ModelSerializer):
    # Borramos la línea de 'user = ...' que tenías aquí arriba ❌
    category_name = serializers.ReadOnlyField(source='category.name')
    type = serializers.CharField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'category', 'category_name', 
            'amount', 'description', 'type', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'date']
    
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
    
    def validate_type(self, value):
        # 1. Normalizamos a mayúsculas
        normalized_type = value.upper()
        print(normalized_type)
        
        # 2. Extraemos los valores permitidos directamente del modelo
        # TRANSACTION_TYPES es una lista de tuplas: [('INCOME', 'Ingreso'), ...]
        # Usamos un list comprehension para sacar solo el primer valor de cada tupla
        valid_options = [choice[0] for choice in Transaction.TRANSACTION_TYPES]
        
        # 3. Validamos contra la lista oficial
        if normalized_type not in valid_options:
            raise serializers.ValidationError(
                f"Tipo inválido. Las opciones permitidas son: {', '.join(valid_options)}."
            )
            
        return normalized_type