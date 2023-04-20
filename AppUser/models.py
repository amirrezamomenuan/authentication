from django.db import models


class AppUser(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)  # TODO: may need to change later

    class Meta:
        db_table = 'app_user'
        verbose_name = 'app user'
        verbose_name_plural = 'app users'


class LoginRequest(models.Model):
    phone_number = models.CharField(max_length=16, db_index=True)
    expire_time = models.DateTimeField()
    verification_code = models.CharField(max_length=8)
    request_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'login_request'
        verbose_name = 'login request'
        verbose_name_plural = 'login requests'
