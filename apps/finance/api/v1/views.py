from rest_framework import viewsets, permissions
from apps.finance.models import Category, Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer, CategorySerializerConJWT
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializerConJWT
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # El usuario ve sus categorías O las globales de los admins
        print(self.request.user.is_staff)
        return Category.objects.filter(
            Q(user=self.request.user) | Q(is_default=True, user__is_staff=True),
        ).order_by('is_default', 'name')        

    def perform_create(self, serializer):
        # 1. Obtenemos el usuario de la petición
        user = self.request.user
        is_default_sent = self.request.data.get('is_default', False) # type: ignore

        if is_default_sent and not user.is_staff:
            raise PermissionDenied("Solo administradores pueden crear categorías globales.")
        
        final_is_default = is_default_sent if user.is_staff else False
        
        # 5. Guardamos con los valores inyectados por nosotros
        serializer.save(user=user, is_default=final_is_default)

    def perform_update(self, serializer):
        instance = self.get_object()
        
        # Si la categoría es global Y el usuario NO es admin
        if instance.is_default and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para editar categorías globales.")
        
        serializer.save()

    def perform_destroy(self, instance):
        if instance.is_default:
            raise PermissionDenied("No puedes eliminar una categoría global.")
        if instance.is_default and not self.request.user.is_staff:
            raise PermissionDenied("No puedes eliminar una categoría global.")
        
        instance.delete()

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)