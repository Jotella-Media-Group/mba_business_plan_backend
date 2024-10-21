from account.models import CustomPermission
from account.models import User
from core.dependency_injection import service_locator
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GroupsSerializer
from .serializers import PermissionSerializer
from .serializers import SendPasswordResetEmailSerializer
from .serializers import SimpleUserAccountSerializer
from .serializers import UserAccountSerializer
from .serializers import UserChangePasswordSerializer
from .serializers import UserLoginSerializer
from .serializers import UserPasswordResetSerializer
from rest_framework import generics


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermissionSerializer
    pagination_class = None
    filterset_fields = ["name", "codename"]

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(CustomPermission).id

        queryset = Permission.objects.filter(
            content_type=content_type).order_by("name")

        return queryset


class GroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.prefetch_related("permissions")
    serializer_class = GroupsSerializer


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class UserAccountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Set is_active to False instead of deleting the user
        instance.is_active = False
        instance.save()

        return Response(
            data="User deactivated successfully", status=status.HTTP_204_NO_CONTENT
        )


class UserAccountListCreateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]


class CreateAccountAPIView(CreateAPIView):
    serializer_class = UserAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        user: User = serializer.save()
        user.set_password(password)
        user.is_active = False
        user.save()

        base_url = self.request.build_absolute_uri("/").rstrip("/")

        account_verification_url = (
            reverse("account:verify_email_view") + f"?user_id={user.id}"
        )

        service_locator.core_service.send_email(
            subject="Email Account Verification",
            template_path="emails/user_login_verification.html",
            template_context={
                "account_verification_url": f"{base_url}{account_verification_url}",
            },
            to_emails=[user.email],
        )

        user_serializer = SimpleUserAccountSerializer(user)

        return Response(
            {"user": user_serializer.data, "token": get_tokens_for_user(user)},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(CreateAPIView):
    """Login a user and generate a token."""

    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)
        existing_user: User = User.objects.filter(email=email).first()

        if user and existing_user:
            user_serializer = SimpleUserAccountSerializer(user)

            return Response(
                {"token": get_tokens_for_user(
                    user), "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )

        if existing_user and not existing_user.is_active:
            return Response(
                data="User account is not active", status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            data="Email or Password is not valid", status=status.HTTP_401_UNAUTHORIZED
        )


class SendPasswordResetEmailView(CreateAPIView):
    """SEND PASSWORD RESET LINK VIA EMAIL"""

    serializer_class = SendPasswordResetEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(data="Password Reset link sent. Please check your Email",
                        status=status.HTTP_200_OK,
                        )


class UserChangePasswordView(CreateAPIView):
    """CHANGE USER PASSWORD"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(data="Password Changed Successfully", status=status.HTTP_200_OK)


class UserPasswordResetView(CreateAPIView):
    serializer_class = UserPasswordResetSerializer

    def create(self, request, *args, **kwargs):
        uid = request.query_params.get("uid", None)
        token = request.query_params.get("token", None)
        serializer = self.get_serializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(data="Password Reset Successfully", status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    def get(
        self,
        request,
    ):
        # get userId from params
        userId = request.query_params.get("user_id", None)
        user = get_user_model().objects.filter(id=userId).first()
        if user is not None:
            # activate user
            user.is_active = True
            user.save()

            # permanent redirect to frontend login page

            return redirect(settings.FRONTEND_URL, permanent=True)
        # send the user to front end 404  page if user not found
        front_end_404 = f"{settings.FRONTEND_URL}/404"
        return redirect(front_end_404)
