from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = [
        ('owner', _('Owner')),
        ('worker', _('Worker')),
    ]
    
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    
    role = models.CharField(_('role'),max_length=10,choices=ROLE_CHOICES,default='worker')
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_CHOICES, blank=True)
    
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    pincode = models.CharField(_('pincode'), max_length=20, blank=True)
    
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    
    employee_id = models.CharField(_('employee ID'), max_length=50, blank=True)
    salary = models.DecimalField(_('salary'), max_digits=10, decimal_places=2, null=True, blank=True)
    
    joining_date = models.DateField(_('joining date'), null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_owner(self):
        return self.role == 'owner'
    
    @property
    def is_worker(self):
        return self.role == 'worker'