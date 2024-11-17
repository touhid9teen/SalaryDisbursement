from django.contrib.auth.backends import ModelBackend
from .models import Users


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            try:
                user = Users.objects.get(email=username)
            except Users.DoesNotExist:
                return None
        else:
            try:
                user = Users.objects.get(contract_number=username)
            except Users.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None