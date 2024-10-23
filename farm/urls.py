from django.urls import path

from farm import views
from rest_framework import routers


app_name = 'farm'


router = routers.DefaultRouter()
router.register("", views.FarmViewSet, "farm")


urlpatterns = [
    path('Property/',
         views.PropertyListViewSet.as_view(), name='farm_data_create'),

    path('Property/<uuid:pk>/',
         views.PropertyUpdateRetrivDestroyViewSet.as_view(), name='farm_data_create'),

    path('Property-create/',
         views.PropertyCreateApiView.as_view(), name='farm_data_create'),
]

urlpatterns += router.urls
