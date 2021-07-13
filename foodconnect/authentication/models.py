from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from core.models import AbstractBaseModel

class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField('Username', max_length=255, unique=True, validators=[username_validator])
    is_active = models.BooleanField('Active', default=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    latitude = models.CharField(max_length=200, default="")
    longitude = models.CharField(max_length=200, default="")
    image = models.CharField(max_length=500, default="")


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # used only on createsuperuser

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def has_perms(self, perm, ob=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.first_name + " " + self.last_name