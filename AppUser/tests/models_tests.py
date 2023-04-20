import pytest
from django.db import IntegrityError

from AppUser.models import AppUser, LoginRequest


pytestmark = pytest.mark.django_db


class TestAppUser:
    def test_creating_users_with_duplicate_phone_numbers(self):
        phone_number = '09123456789'

        AppUser.objects.create(phone_number=phone_number)

        try:
            AppUser.objects.create(phone_number=phone_number)
        except IntegrityError:
            assert True
        else:
            assert False
