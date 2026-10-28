from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # Hacemos copia mutable en caso de que request.data sea un QueryDict inmutable
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True
        if 'password' in request.data and request.data['password']:
            request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True

        # CORRECCIÓN DE SEGURIDAD 2:
        # El manual tenía el error grave de asignar `request.data["password"] = request.user.password`
        # en el bloque `else`, lo que provocaba que al editar cualquier usuario sin enviar contraseña,
        # se le sobrescribiera su contraseña con la del administrador que hacía la petición.
        # Solución: Solo hashear y actualizar si 'password' viene con valor en la petición;
        # de lo contrario, eliminar la clave o ignorarla para conservar la contraseña actual del usuario.
        password = request.data.get('password', None)
        if password:
            request.data['password'] = make_password(password)
        elif 'password' in request.data:
            request.data.pop('password')

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True

        password = request.data.get('password', None)
        if password:
            request.data['password'] = make_password(password)
        elif 'password' in request.data:
            request.data.pop('password')

        return super().update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
