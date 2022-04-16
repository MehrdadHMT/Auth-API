from django.core.exceptions import ValidationError
from user_agents import parse

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
    except AttributeError as e:
        raise(e)

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist as e:
        raise(e)

    token.user_agent = user_agent
    token.save()
