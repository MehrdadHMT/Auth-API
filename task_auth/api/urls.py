from django.urls import path, include
from rest_framework.authtoken import views
# from rest_framework import routers

from task_auth.api.views import (UserRegisterView, UserLoginView, UserLogoutView,TokensListView,
                                 KillTokensView, SendOTPView, OTPValidationView, ChangePasswordView,
                                 ForgotPasswordView)


# router = routers.DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="api_user_register"),
    path("login/", UserLoginView.as_view(), name="api_user_login"),
    path("logout/", UserLogoutView.as_view(), name="api_user_logout"),
    path("list-tokens/", TokensListView.as_view(), name="api_list_tokens"),
    path("kill-tokens/", KillTokensView.as_view(), name="api_kill_tokens"),
    path("send-otp/", SendOTPView.as_view(), name="api_send_otp"),
    path("validate-otp/", OTPValidationView.as_view(), name="api_validate_otp"),
    path("change-pass/", ChangePasswordView.as_view(), name="api_change_pass"),
    path("forgot-pass/", ForgotPasswordView.as_view(), name="api_forgot_pass"),
]

# urlpatterns += [
#     path("auth/", include("rest_framework.urls")),
#     path("token-auth/", views.obtain_auth_token, name='api-token-auth')
# ]