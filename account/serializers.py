from account.models import CustomPermission
from account.models import User
from core.dependency_injection import service_locator
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import force_bytes
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from django.conf import settings


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "content_type": {"read_only": True},
            "codename": {"read_only": True},
        }

    def create(self, validated_data):
        content_type = ContentType.objects.get_for_model(CustomPermission).id

        name = validated_data.get("name")
        codename = validated_data.get("name").lower()

        custom_permission = Permission.objects.create(
            codename=codename.replace(" ", "_").lower(),
            name=name,
            content_type_id=content_type,
        )

        return custom_permission


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "pk": {"read_only": True, "permissions": {"write_only": True}},
        }

    def to_representation(self, instance: Group):
        ret = super().to_representation(instance)
        ret["permissions"] = PermissionSerializer(
            instance.permissions.all(), many=True
        ).data
        return ret


class UserAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        exclude = ["user_permissions"]
        read_only_fields = ["id", "is_superuser"]

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True, "required": True},
            "is_superuser": {"read_only": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password_2")

        if password and password2:
            if password != password2:
                raise serializers.ValidationError(
                    code="password2",
                    detail="Password and Confirm Password do not match"
                )
            try:
                validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError(
                    code="password", detail=e.messages)

        return super().validate(attrs)

    def to_representation(self, instance: User):
        ret = super().to_representation(instance)
        ret["groups"] = GroupsSerializer(instance.groups.all(), many=True).data
        return ret


class SimpleUserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "address",
            "gender",
            "is_active",
            "profile"
        ]

    def to_representation(self, instance: User):
        ret = super().to_representation(instance)
        ret["groups"] = GroupsSerializer(instance.groups.all(), many=True).data
        return ret


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password_2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                code='invalid_password', detail="Password and Confirm Password doesn't match"
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(
                code='password', detail=e.messages)
        user.set_password(password)
        user.save()
        return attrs


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # Send EMail

            service_locator.core_service.send_email(
                subject="Reset Your Password for {}".format(user.email),
                template_path="emails/password_reset_link.html",
                template_context={
                    "user": user,
                    "password_reset_link": f"{settings.FRONTEND_URL}set-new-password/?uid={uid}&token={token}",
                    "body": "Click Following Link to set a new Password",
                },
                to_emails=[user.email],
            )
            return attrs
        else:
            raise serializers.ValidationError(
                code='invalid_user', detail="You are not a Registered User")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )

    class Meta:
        fields = ["password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True, "required": True},
        }

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = self.initial_data.get("password_2")

            uid = self.context.get("uid")
            token = self.context.get("token")

            if password != password2:
                raise serializers.ValidationError(
                    code="set_password",
                    detail="Password and Confirm Password don't match"
                )

            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    code='token_invalid', detail="Token is not Valid or Expired")

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError(
                code="token_invalid", detail="Token is not Valid or Expired")
