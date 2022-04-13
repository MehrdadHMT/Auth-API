from django.apps import AppConfig


class UaMiddlewareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_agent_middleware'
