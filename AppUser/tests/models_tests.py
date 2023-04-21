import pytest
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError

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
    def test_1(self):
        assert True
