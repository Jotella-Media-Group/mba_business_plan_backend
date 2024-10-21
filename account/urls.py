from django.urls import path

from account import views

from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from rest_framework import routers

app_name = 'account'

router = routers.DefaultRouter()
router.register("groups", views.GroupsViewSet, "groups")
router.register("permissions", views.PermissionViewSet, "permissions")

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),

    path('signup/', views.CreateAccountAPIView.as_view(), name='signup_user'),
    path('users/', views.UserAccountListCreateView.as_view(), name='list_account'),

    path('users/<uuid:pk>/', views.UserAccountRetrieveUpdateDestroyView.as_view(),
         name='user_account_retrieve_update_destroy'),

    path('change-password/', views.UserChangePasswordView.as_view(),
         name='changepassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
    path('reset-password/', views.UserPasswordResetView.as_view(),
         name='reset-password'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "verify_email/",
        views.VerifyEmailView.as_view(),
        name="verify_email_view",
    ),

]

urlpatterns += router.urls
