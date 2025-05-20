from django.http import HttpResponseRedirect
from django.urls import reverse

class NoSuccessMessageAdminMixin:

    def message_user(self, *args, **kwargs):
        pass