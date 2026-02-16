from rest_framework import serializers
from apps.finance.models import Category
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializerConJWT(serializers.ModelSerializer):
    # Esta es la pieza clave: toma el usuario del contexto (el Token)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        # Agregamos 'user' aquí para que el validador lo vea internamente
        fields = ['id', 'name', 'icon', 'is_default', 'created_at', 'user']
        read_only_fields = ['id', 'created_at']

        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['user', 'name'],
                message="Ya tienes una categoría con este nombre."
            )
        ]

    def validate_icon(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(f"Icono demasiado largo ({len(value)}/50).")
        if not value.strip():
            raise serializers.ValidationError("El icono no puede estar vacío.")
        return value
