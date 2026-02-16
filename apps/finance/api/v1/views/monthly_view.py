from rest_framework import permissions
from ..serializers.montyly_serializers import MonthlySummarySerializer
from apps.finance.models import Budget, Transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema

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