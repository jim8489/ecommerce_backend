from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .jwt import (
    CustomTokenObtainPairSerializer,
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
)

from .services import UserService


class RegisterAPIView(
    generics.CreateAPIView,
):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(
        self,
        serializer,
    ):
        UserService.register(
            serializer.validated_data
        )


class LoginAPIView(
    TokenObtainPairView,
):
    serializer_class = (
        CustomTokenObtainPairSerializer
    )


class ProfileAPIView(
    generics.RetrieveUpdateAPIView,
):

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):
        return self.request.user