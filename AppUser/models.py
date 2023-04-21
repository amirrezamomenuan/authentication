import random
import string

from django.db import models
from django.conf import settings
from django.core.validators import validate_integer
from django.utils import timezone
from django.core.exceptions import ValidationError


class LoginRequestManager(models.Manager):
    def create(self, *args, **kwargs):
        raise PermissionError(
            'calling create() is not allowed, use save() method on the model to create new objects'
        )


class AppUser(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)  # TODO: may need to change later

    class Meta:
        db_table = 'app_user'
        verbose_name = 'app user'
        verbose_name_plural = 'app users'

    def clean(self):
        validate_integer(self.phone_number)
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class LoginRequest(models.Model):
    phone_number = models.CharField(max_length=16, db_index=True)
    expire_time = models.DateTimeField()
    verification_code = models.CharField(max_length=8)
    request_date = models.DateField(auto_now_add=True, db_index=True)
    objects = LoginRequestManager()

    class Meta:
        db_table = 'login_request'
        verbose_name = 'login request'
        verbose_name_plural = 'login requests'

    @classmethod
    def __check_request_limits(cls, phone_number: str):
        last_login_requests = list(
            cls.objects.filter(
                phone_number=phone_number
            )
        )
        if not last_login_requests:
            return
        elif len(last_login_requests) >= settings.LOGIN_REQUEST_LIMIT:
            raise ValidationError('login request limit reached for today')
        elif last_login_requests[-1].expire_time > timezone.now():
            raise ValidationError('already sent a verification code')

    @staticmethod
    def __generate_verification_code():
        return ''.join(random.choices(string.digits, k=settings.VERIFICATION_CODE_LENGTH))

    def clean(self):
        validate_integer(self.phone_number)
        self.__check_request_limits(self.phone_number)

        super().clean()

    def save(self, *args, **kwargs):
        self.verification_code = self.__generate_verification_code()
        self.expire_time = timezone.now() + timezone.timedelta(
            seconds=settings.VERIFICATION_CODE_EXPIRE_TIME_SECONDS
        )

        self.full_clean()

        super().save(*args, **kwargs)
