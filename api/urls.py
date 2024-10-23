from django.urls import include
from django.urls import path

urlpatterns = [
    path('accounts/', include("account.urls")),
    path('farms/', include("farm.urls")),



]
