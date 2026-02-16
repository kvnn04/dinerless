from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from ..serializers.budget_serializer import BudgetSerializer, MonthlySummarySerializer
from apps.finance.models import Budget, Transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
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
        

@extend_schema(tags=['Resumen mesual'])
class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Obtener resumen financiero mensual",
        responses={200: MonthlySummarySerializer}
    )

    def get(self, request):
        user = request.user
        now = timezone.now()
        month = now.month
        year = now.year

        transactions = Transaction.objects.filter(user=user, date__month=month, date__year=year)
        
        ingresos = transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        gastos = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0

        presupuestos_alerta = []
        budgets = Budget.objects.filter(user=user, month=month, year=year)

        for budget in budgets:
            gastado_cat = transactions.filter(
                category=budget.category, 
                type='EXPENSE'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            progreso_val = (gastado_cat / budget.limit_amount) * 100 if budget.limit_amount > 0 else 0
            
            presupuestos_alerta.append({
                "categoria": budget.category.name,
                "limite": budget.limit_amount,
                "gastado": gastado_cat,
                "progreso": f"{round(progreso_val, 2)}%"
            })

        data = {
            "mes": now.strftime("%B %Y"), # Ejemplo: "February 2026"
            "total_ingresos": ingresos,
            "total_gastos": gastos,
            "balance": ingresos - gastos,
            "presupuestos_alerta": presupuestos_alerta
        }

        return Response(data)