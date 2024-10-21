from rest_framework import serializers


class CreatedByMixin:
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        return super().create(validated_data)


class AbstractSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = "__all__"
        depth = 1


class BaseToRepresentation:
    def to_representation(self, instance):
        serializer = AbstractSerializer(instance=instance)
        serializer.Meta.model = instance.__class__
        return serializer.data if instance else {}
