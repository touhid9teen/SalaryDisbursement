import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UUIDField


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        '''Creates and saves a new superuser'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure user_type is set to 'admin' if not provided
        if extra_fields.get('user_type') is None:
            extra_fields['user_type'] = 'admin'

        return self.create_user(email, password, **extra_fields)



class Users(AbstractUser):

    USER_TYPES = (
        ('manager', 'Manager'),
        ('employ', 'Employ'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    contract_number = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    password = models.CharField(max_length=100)
    conform_password = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    company_id = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
