from django.urls import path, include
from rest_framework.authtoken import views
# from rest_framework import routers

from task_auth.api.views import UserRegisterView, UserLoginView, UserLogoutView


# router = routers.DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="api_user_register"),
    path("login/", UserLoginView.as_view(), name="api_user_login"),
    path("logout/", UserLogoutView.as_view(), name="api_user_logout"),
]

# urlpatterns += [
#     path("auth/", include("rest_framework.urls")),
#     path("token-auth/", views.obtain_auth_token, name='api-token-auth')
# ]