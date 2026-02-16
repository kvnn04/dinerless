from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from ..serializers.budget_serializer import BudgetSerializer
from apps.finance.models import Budget

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Aseguramos que solo vea SUS presupuestos
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 1. Validamos la categoría antes de crear
        self._validate_budget_data(serializer)
        # 2. Asignamos al usuario dueño del token
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # En el update, solo permitimos cambiar el MONTO (amount)
        # Obtenemos la instancia actual (lo que hay en la DB)
        instance = self.get_object()
        
        # Guardamos forzando que los campos sensibles no cambien
        serializer.save(
            user=instance.user,
            category=instance.category,
            month=instance.month,
            year=instance.year
        )

    def _validate_budget_data(self, serializer):
        user = self.request.user
        category = serializer.validated_data.get('category')
        month = serializer.validated_data.get('month')
        year = serializer.validated_data.get('year')

        # 1. Validar que la categoría sea suya o global
        if category and category.user != user and not category.is_default:
            raise ValidationError({"category": "No tienes permiso para usar esta categoría."})

        # 2. Validar que no exista ya un presupuesto para esa categoría/mes/año
        # Esto evita duplicados
        exists = Budget.objects.filter(
            user=user,
            category=category,
            month=month,
            year=year
        ).exists()

        if exists:
            raise ValidationError("Ya tienes un presupuesto configurado para esta categoría en este periodo.")