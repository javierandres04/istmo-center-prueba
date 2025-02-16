from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Apply the Admin role when a superuser is created from the command line
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USER', 'User'
        ADMIN = 'ADMIN', 'Admin'
    
    role = models.CharField(max_length=5, choices=Role.choices, default=Role.USER)
    email = models.EmailField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
   
    objects = UserManager()

    username = None # Remove the email field from the parent class

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def save(self, *args, **kwargs):
        # If the user is an admin, set is_staff
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
