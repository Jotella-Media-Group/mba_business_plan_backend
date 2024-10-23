

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from farm.models import Farm, Property
from farm.serializers import FarmSerializer, PropertySerializer, PropertyCreateSerializer
import pandas as pd
from django.db import transaction
from farm.filters import PropertyFilter, FarmFilter


class FarmViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Farm.objects.order_by('-created_at')
    serializer_class = FarmSerializer
    filterset_class = FarmFilter


class PropertyListViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.order_by('-created_at')
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter


class PropertyUpdateRetrivDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.order_by('-created_at')
    serializer_class = PropertySerializer


class PropertyCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertyCreateSerializer
    queryset = Property.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        farm_serializer = FarmSerializer(
            data=serializer.validated_data,
            context=self.get_serializer_context()
        )
        farm_serializer.is_valid(raise_exception=True)
        farm = farm_serializer.save()

        try:
            if file.name.endswith('.csv'):
                data_frame = pd.read_csv(file)
            else:
                data_frame = pd.read_excel(file)

            properties_to_create = []

            for _, row in data_frame.iterrows():
                property_data = {
                    "farm": farm,
                    "created_by": user,
                    **row.to_dict()
                }
                properties_to_create.append(Property(**property_data))

            Property.objects.bulk_create(properties_to_create)

            return Response({"message": "Properties created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
