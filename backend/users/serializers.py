from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'matricula',
            'carrera',
            'password',
            'is_active',
            'is_staff',
        ]
        # CORRECCIÓN DE SEGURIDAD 1:
        # Se configura 'password' como write_only=True para que el hash de la contraseña
        # NUNCA se exponga en las respuestas JSON de la API (ni en el CRUD ni en /auth/me/),
        # y required=False para permitir actualizaciones parciales sin exigir contraseña.
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
