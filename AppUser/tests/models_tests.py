from unittest import mock

import pytest
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

from AppUser.models import AppUser, LoginRequest


pytestmark = pytest.mark.django_db


class TestAppUser:
    @pytest.mark.parametrize(
        'phone_number, creation_should_pass', [
            ('ve879o 2 92', False),
            ('0632489567610394850649170984254109', False),
            ('09123456789', True),
            ('+989123456789', False),
            ('', False),
        ]
    )
    def test_phone_number_characters_validation(
            self,
            phone_number,
            creation_should_pass
    ):
        try:
            AppUser.objects.create(phone_number=phone_number)
        except (DataError, ValidationError):
            if creation_should_pass:
                assert False
        else:
            if not creation_should_pass:
                assert False


class TestLoginRequest:
    @pytest.mark.parametrize(
        'phone_number, creation_should_pass', [
            ('ve879o 2 92', False),
            ('0632489567610394850649170984254109', False),
            ('09123456789', True),
            ('+989123456789', False),
            ('', False),
        ]
    )
    def test_phone_number_characters_validation(
            self,
            phone_number,
            creation_should_pass
    ):
        try:
            LoginRequest(
                phone_number=phone_number,
            ).save()
        except (DataError, ValidationError):
            if creation_should_pass:
                assert False
        else:
            if not creation_should_pass:
                assert False

    @pytest.mark.parametrize(
        'second_call_after_expiration, creation_should_pass',[
            (True, True),
            (False, False)
        ]
    )
    def test_creating_a_new_instance_with_different_expiration_times(
            self,
            second_call_after_expiration,
            creation_should_pass
    ):
        phone_number = '09123456789'
        current_time = timezone.now()
        expiration_limit = timezone.timedelta(
            seconds=settings.VERIFICATION_CODE_EXPIRE_TIME_SECONDS
        )

        with mock.patch('AppUser.models.timezone') as tz_mock:
            tz_mock.now.return_value = current_time
            tz_mock.timedelta.return_value = expiration_limit

            LoginRequest(
                phone_number=phone_number,
            ).save()

            if second_call_after_expiration:
                tz_mock.now.return_value = current_time + expiration_limit

            try:
                LoginRequest(
                    phone_number=phone_number,
                ).save()
            except ValidationError:
                if creation_should_pass:
                    assert False
            else:
                if not creation_should_pass:
                    assert False

    def test_instance_creation_limit_per_day(self):
        phone_number = '09123456789'
        current_time = timezone.now()
        expiration_limit = timezone.timedelta(
            seconds=settings.VERIFICATION_CODE_EXPIRE_TIME_SECONDS
        )

        with mock.patch('AppUser.models.timezone') as tz_mock:
            tz_mock.timedelta.return_value = expiration_limit

            for i in range(settings.LOGIN_REQUEST_LIMIT + 1):
                tz_mock.now.return_value = current_time
                current_time += expiration_limit

                try:
                    LoginRequest(
                        phone_number=phone_number,
                    ).save()
                    if i == settings.LOGIN_REQUEST_LIMIT:
                        assert False
                except ValidationError:
                    if i != settings.LOGIN_REQUEST_LIMIT:
                        assert False
