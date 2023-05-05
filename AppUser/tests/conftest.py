import pytest

from AppUser.models import LoginRequest


@pytest.fixture
def login_request():
    _login_request = LoginRequest(phone_number='09123456789')
    _login_request.save()
    return _login_request