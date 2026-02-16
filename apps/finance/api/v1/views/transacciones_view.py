from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.finance.models import Transaction
from ..serializers.transaction_serializer import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar Transacciones:
    - GET: Lista solo las transacciones del usuario.
    - POST: Crea una transacción asociada al usuario del JWT.
    - GET /id/: Detalle de una transacción (si es propia).
    - PATCH/PUT /id/: Actualiza una transacción (validando categoría).
    - DELETE /id/: Elimina una transacción (si es propia).
    """
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # EL CANDADO DE LECTURA: 
        # Nadie ve lo que no es suyo. El ID de la URL se busca solo aquí.
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        # EL CANDADO DE CREACIÓN:
        # 1. Validamos la categoría elegida
        self._validate_category(serializer)
        # 2. Inyectamos el usuario automáticamente
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # EL CANDADO DE ACTUALIZACIÓN:
        # Validamos que si cambian la categoría, sea una válida
        self._validate_category(serializer)
        serializer.save()

    def _validate_category(self, serializer):
        """
        Método auxiliar para no repetir código.
        Valida que la categoría pertenezca al usuario o sea global.
        """
        category = serializer.validated_data.get('category')
        user = self.request.user
        
        if category:
            # Si la categoría no es del usuario Y no es por defecto (global)
            if category.user != user and not category.is_default:
                raise ValidationError(
                    {"category": "No tienes permiso para usar esta categoría o no existe."}
                )