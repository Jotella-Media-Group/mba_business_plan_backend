from rest_framework import serializers
from farm.models import Farm, Property
import os
from core.serializers import CreatedByMixin


class FarmSerializer(CreatedByMixin, serializers.ModelSerializer):

    class Meta:
        model = Farm
        exclude = ['is_deleted']
        read_only_fields = ['id', 'created_by']


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        exclude = ['is_deleted']


class PropertyCreateSerializer(CreatedByMixin, serializers.ModelSerializer):
    VALID_EXTENSIONS = ["xls", "xlsx", "csv"]

    file = serializers.FileField(
        write_only=True,
        help_text="Upload farm data (xlsx, xls, csv)",
        required=True,
    )

    class Meta:
        model = Farm
        exclude = ['is_deleted']
        read_only_fields = ['id', 'created_by']

    def validate(self, data):
        file = data.get("file")

        if not file:
            raise serializers.ValidationError("Please specify a file.")

        file_name, file_extension = os.path.splitext(file.name)
        file_extension = file_extension.lower().lstrip(".")

        if file_extension not in self.VALID_EXTENSIONS:
            raise serializers.ValidationError(
                f"Invalid file format. Supported formats are: {
                    ', '.join(self.VALID_EXTENSIONS)}."
            )

        data["extension"] = file_extension
        return data
