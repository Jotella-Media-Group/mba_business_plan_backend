from django_filters import rest_framework as filters
from farm.models import Property, Farm


class FarmFilter(filters.FilterSet):

    class Meta:
        model = Farm
        fields = [
            "name", "city", "description", "created_by"
        ]


class PropertyFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Property
        fields = {
            'farm': ['exact'],
            'created_by': ['exact'],
            'ownerfirst': ['iexact'],
            'ownerlast': ['iexact'],
            'siteaddres': ['iexact'],
            'sitestate': ['iexact'],
            'sitecity': ['iexact'],
            'sitezip': ['iexact'],
            'mailaddres': ['iexact'],
            'mailcity': ['iexact'],
            'mailstate': ['iexact'],
            'mzipandzip': ['iexact'],
            'bedrooms': ['exact'],
            'bathtot': ['exact'],
            'totalsf': ['exact'],
            'lotsqft': ['exact'],
            'landuse': ['exact'],
            'notes': ['icontains'],
        }
