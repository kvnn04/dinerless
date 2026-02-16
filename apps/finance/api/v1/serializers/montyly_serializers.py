from rest_framework import serializers

class BudgetProgressSerializer(serializers.Serializer):
    categoria = serializers.CharField()
    limite = serializers.DecimalField(max_digits=10, decimal_places=2)
    gastado = serializers.DecimalField(max_digits=10, decimal_places=2)
    progreso = serializers.CharField() # Ejemplo: "90%"

class MonthlySummarySerializer(serializers.Serializer):
    mes = serializers.CharField()
    total_ingresos = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_gastos = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    presupuestos_alerta = BudgetProgressSerializer(many=True)