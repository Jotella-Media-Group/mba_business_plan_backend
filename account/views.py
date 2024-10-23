from account.models import User
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView

from account.serializers import TokenSerializer, UserSerializer

import jwt
from django.shortcuts import get_object_or_404


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.prefetch_related("permissions")
    serializer_class = UserSerializer


class DecodeTokenView(CreateAPIView):
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token')
        try:
            decoded_token = jwt.decode(
                token, settings.BPO_HOMES_SECRET_KEY, algorithms=["HS256"])
            email = decoded_token.get('user_id')

            if not email:
                return Response(data='Invalid token provided', status=status.HTTP_400_BAD_REQUEST)

            user, _ = User.objects.get_or_create(email=email)

            token = get_tokens_for_user(user)

            data = {
                "token": token,
                "frontend_url": settings.FRONTEND_URL
            }
            return Response(data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DecodeMBATokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ** kwargs):

        try:

            decoded_token = jwt.decode(
                kwargs.get('token'), settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')

            user = get_object_or_404(User, id=user_id)

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
