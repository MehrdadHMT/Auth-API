from django.urls import path, include
from rest_framework.authtoken import views
# from rest_framework import routers

from task_auth.api.views import register_user, user_login, user_logout, current_user


# router = routers.DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    # path("register/", UserRegisterView.as_view(), name="api_user_register"),
    path("register/", register_user, name="api_user_register"),
    path("login/", user_login, name="api_user_login"),
    path("logout/", user_logout, name="api_user_logout"),
    # path("current_user/", current_user)
]

# urlpatterns += [
#     path("auth/", include("rest_framework.urls")),
#     path("token-auth/", views.obtain_auth_token, name='api-token-auth')
# ]