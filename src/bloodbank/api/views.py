from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from bloodbank.models import BloodCatalog
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    BloodCatalogListSerializer,
    BloodCatalogDetailSerializer,
    BloodCatalogCreateUpdateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
)

User = get_user_model()


class BloodCatalogCreateAPIView(CreateAPIView):
    queryset = BloodCatalog.objects.all()
    serializer_class = BloodCatalogCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BloodCatalogListAPIView(ListAPIView):
    queryset = BloodCatalog.objects.all()
    serializer_class = BloodCatalogListSerializer
    permission_classes = [AllowAny]


class BloodCatalogDetailAPIView(RetrieveAPIView):
    queryset = BloodCatalog.objects.all()
    serializer_class = BloodCatalogDetailSerializer
    permission_classes = [AllowAny]


class BloodCatalogUpdateAPIView(RetrieveUpdateAPIView):
    queryset = BloodCatalog.objects.all()
    serializer_class = BloodCatalogCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):

    def get(self, request, *args, **kwargs):
        request.user.token.delete()
        return Response(status=HTTP_200_OK)
