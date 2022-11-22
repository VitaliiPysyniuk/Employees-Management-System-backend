from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUserModel(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    class Role(models.TextChoices):
        ADMINISTRATOR = ('ad', _('admin'))
        EMPLOYEE = ('em', _('employee'))

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message='The first name can contain only latin letters.')
    ])
    last_name = models.CharField(max_length=30, blank=True, validators=[
        RegexValidator(regex=r'^[A-Za-z]*$', message='The last name can contain only latin letters.')
    ])
    current_position = models.CharField(max_length=60)
    is_active = models.BooleanField(default=False)
    company_join_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.EMPLOYEE)

    is_superuser = None
    groups = None
    user_permissions = None
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class ReviewModel(models.Model):
    class Meta:
        db_table = 'reviews'

    description = models.CharField(max_length=200, blank=True)
    position_before = models.CharField(max_length=60, blank=True)
    position_after = models.CharField(max_length=60, blank=True)
    salary_change = models.IntegerField(default=0)
    review_date = models.DateField()

    employee = models.ForeignKey(CustomUserModel, on_delete=models.PROTECT, related_name='reviews')
