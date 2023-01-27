from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import PermissionsMixin
from .user_manager import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, blank=False)
    reset_password_token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    date_joined = models.DateTimeField(
        ('date joined'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name}, {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return ''

    def is_administrator(self):
        return self.is_superuser or self.is_staff

    def full_name_no_comma(self):
        return f"{self.first_name.lower()} {self.last_name.lower()}"


def player_directory_path(instance, filename):
    return 'pictures/{1}(id:{0})/{2}'.format(instance.user.id, instance.user.full_name(), filename)


class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex='/^(?:[0-8]\d|9[0-8])\d{3}$/',
            message='Phone number should be  8 or 13 digits long and can optionally be preceded by the country code followed by a space or a coma.',
            code='invalid_phone_number'
        )
    ])
    restaurant_name = models.CharField(max_length=100, blank=True)
    restaurant_address = models.CharField(max_length=150, blank=True)
    restaurant_city = models.CharField(max_length=35, blank=True)
    restaurant_postal_code = models.CharField(max_length=7, blank=True)
    checking_picture = models.CharField(max_length=100, blank=True)
    to_contact_when_product_is_out = models.FileField(
        upload_to=player_directory_path)
    points = models.IntegerField(default=0, validators=[
                                 MinValueValidator(limit_value=0)])


class IntroductionFormAnswer(models.Model):
    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
