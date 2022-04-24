from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from task_auth.models import Token


def get_user_agent(request):
    if not hasattr(request, 'META'):
        return ''

    ua_string = request.META.get('HTTP_USER_AGENT', '')

    if not ua_string:
        raise ValidationError({"message": "User request must have 'User_Agent' header"})

    if not isinstance(ua_string, str):
        ua_string = ua_string.decode('utf-8', 'ignore')

    # user_agent = parse(ua_string)

    return ua_string


def save_ua_in_db(request):
    user_agent = str(request.user_agent)
    try:
        token_key = request.headers.get('Authorization').split()[-1]
    except AttributeError:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    token.user_agent = user_agent
    token.save()
