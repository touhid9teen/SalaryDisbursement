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

    '''create superuser '''
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Users(AbstractUser):

    USER_TYPES = (
        ('manager', 'Manager'),
        ('employ', 'Employ'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contract_number = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.BooleanField(default=False)
    address = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contract_number', 'user_type']


    def __str__(self):
        return self.email
