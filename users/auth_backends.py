# from django.contrib.auth.backends import ModelBackend
# from .models import Users
#
#
# class EmailOrPhoneBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if '@' in username:
#             try:
#                 user = Users.objects.get(email=username)
#             except Users.DoesNotExist:
#                 return None
#         else:
#             try:
#                 user = Users.objects.get(username=username)
#             except Users.DoesNotExist:
#                 return None
#
#         if user.check_password(password):
#             return user
#         return None
#

# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Users  # Ensure this is the correct model name

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, phone=None, **kwargs):
        # Log input parameters
        print(f"Authenticating with username={username}, phone={phone}, password={password}")

        # Try to authenticate using phone if provided
        if phone:
            try:
                user = Users.objects.get(phone=phone)
                print(f"User found by phone: {user}")
            except Users.DoesNotExist:
                print("No user found by phone.")
                return None
        elif '@' in username:
            # Try to authenticate using email if '@' is in the username
            try:
                user = Users.objects.get(email=username)
                print(f"User found by email: {user}")
            except Users.DoesNotExist:
                print("No user found by email.")
                return None
        else:
            # Try to authenticate using username if no email or phone
            try:
                user = Users.objects.get(username=username)
                print(f"User found by username: {user}")
            except Users.DoesNotExist:
                print("No user found by username.")
                return None

        # Check if the password matches
        if user and user.check_password(password):
            print(f"Password is correct for user: {user}")
            return user
        else:
            print("Invalid password or user not found.")
            return None  # Return None if password is incorrect or no user is found
