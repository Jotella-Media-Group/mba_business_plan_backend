from django.urls import path

from account import views
from rest_framework import routers


app_name = 'account'


router = routers.DefaultRouter()
router.register("users", views.UserViewSet, "users")

urlpatterns = [


    path('decode-token/', views.DecodeTokenView.as_view(), name='decode-token'),
    path('decode-token/<str:token>/',
         views.DecodeMBATokenView.as_view(), name='decode-mc-token'),


]

urlpatterns += router.urls
