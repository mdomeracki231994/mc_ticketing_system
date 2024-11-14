# app_user/models.py
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from Apps.org_management.models import Organization


class AppUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            password=None,
            first_name=None,
            last_name=None,
            is_active=False,
            is_staff=False,
            is_site_owner=False,
            org_id = None,
    ):
        if not email:
            raise ValueError("An Email is required")
        if not password:
            raise ValueError("A Password is required")
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_site_owner=is_site_owner,
            org_id=org_id,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("An Email is required")
        if not password:
            raise ValueError("A Password is required")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    SITE_OWNER = 1
    SITE_ADMIN = 2
    MANAGER = 3
    BASE_EMPLOYEE = 4
    FULL_EMPLOYEE = 5

    ROLE_CHOICES = (
        (SITE_OWNER, "Site Owner"),
        (SITE_ADMIN, "Site Admin"),
        (MANAGER, "Manager"),
        (BASE_EMPLOYEE, "Base Employee"),
        (FULL_EMPLOYEE, "Full Employee"),
    )
    current_active_project = models.PositiveSmallIntegerField(default=1)
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=55, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=SITE_ADMIN)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}  {self.email}'
