from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be provided.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        # Bypass 'username' field and ensure only 'email' is used
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Disable the username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"  # Set email as the username field
    REQUIRED_FIELDS = []  # No additional required fields for superuser creation

    objects = CustomUserManager()

    def __str__(self):
        return self.email
