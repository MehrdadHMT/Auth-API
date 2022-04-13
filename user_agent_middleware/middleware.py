from django.utils.functional import SimpleLazyObject
from django.urls import reverse

from .utils import get_user_agent, save_ua_in_db


class UserAgentMiddleware(object):

    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            return None
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))

        # if request.user.is_authenticated:
        if request.headers.get('Authorization') is not None:
            save_ua_in_db(request)
