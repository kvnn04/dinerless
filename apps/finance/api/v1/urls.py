from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.categorias_view import CategoryViewSet
from .views.budget_view import BudgetViewSet
from .views.transacciones_view import TransactionViewSet
# from .views import CategoryViewSet, TransactionViewSet, BudgetViewSet
from .views.budget_view import MonthlySummaryView

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')


urlpatterns = [
    # Ruta manual para el resumen
    path('summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    
    path('', include(router.urls)),

]