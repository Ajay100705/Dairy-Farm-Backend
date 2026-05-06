
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for creating users with email as username.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('Email address is required'))
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_owner(self, email, password=None, **extra_fields):
        """
        Create and save an owner user.
        """
        extra_fields.setdefault('role', 'owner')
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, **extra_fields)
    
    def create_worker(self, email, password=None, **extra_fields):
        """
        Create and save a worker user.
        """
        extra_fields.setdefault('role', 'worker')
        extra_fields.setdefault('is_verified', False)
        return self.create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'owner')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)
