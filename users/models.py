from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USER', 'User'
        ADMIN = 'ADMIN', 'Admin'
    
    role = models.CharField(max_length=5, choices=Role.choices, default=Role.USER)
    username = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
   

    def save(self, *args, **kwargs):
        # If the user is an admin, set is_staff
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)