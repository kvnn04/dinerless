from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from ..serializers.budget_serializer import BudgetSerializer
from apps.finance.models import Budget
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Presupuestos'])
class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        self._validate_budget_data(serializer)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
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

        if category and category.user != user and not category.is_default:
            raise ValidationError({"category": "No tienes permiso para usar esta categoría."})

        exists = Budget.objects.filter(
            user=user,
            category=category,
            month=month,
            year=year
        ).exists()

        if exists:
            raise ValidationError("Ya tienes un presupuesto configurado para esta categoría en este periodo.")
        
