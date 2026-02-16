from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from apps.finance.models import Category
from django.db.models import Q
from ..serializers.category_serializer import CategorySerializerConJWT
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Categorias'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerConJWT
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # El usuario ve sus categorías O las globales de los admins
        print(self.request.user.is_staff)
        return Category.objects.filter(
            Q(user=self.request.user) | Q(is_default=True, user__is_staff=True),
        ).order_by('is_default', 'name')        

    def perform_create(self, serializer):
        user = self.request.user
        is_default_sent = self.request.data.get('is_default', False) # type: ignore

        if is_default_sent and not user.is_staff:
            raise PermissionDenied("Solo administradores pueden crear categorías globales.")
        
        final_is_default = is_default_sent if user.is_staff else False
        
        # 5. Guardamos con los valores inyectados por nosotros
        serializer.save(user=user, is_default=final_is_default)

    def perform_update(self, serializer):
        instance = self.get_object()
        
        if instance.is_default and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para editar categorías globales.")
        
        serializer.save()

    def perform_destroy(self, instance):
        if instance.is_default:
            raise PermissionDenied("No puedes eliminar una categoría global.")
        if instance.is_default and not self.request.user.is_staff:
            raise PermissionDenied("No puedes eliminar una categoría global.")
        
        instance.delete()