from django.urls import path


from .views import (UserRegisterView, UserLoginView, UserLogoutView, TokensListView, KillTokensView, SendOTPView,
                    OTPValidationView, ChangePasswordView, ForgotPasswordView)


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
