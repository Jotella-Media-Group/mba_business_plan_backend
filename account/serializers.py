from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
