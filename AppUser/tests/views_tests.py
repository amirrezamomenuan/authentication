from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

from django.db import models


pytestmark = pytest.mark.django_db


class TestLoginViewStep1:
    @pytest.mark.parametrize(
        'phone_number, expected_status_code, send_sms', [
            ('09123456789', status.HTTP_201_CREATED, True),
            ('', status.HTTP_400_BAD_REQUEST, False),
            (123, status.HTTP_400_BAD_REQUEST, False),
            (None, status.HTTP_400_BAD_REQUEST, False),
            ('0916506898418516584', status.HTTP_400_BAD_REQUEST, False),
            ('abcd', status.HTTP_400_BAD_REQUEST, False),
        ]
    )
    @mock.patch('AppUser.views.send_verification_sms')
    def test_with_providing_different_phone_numbers(
            self,
            send_verification_sms_mock,
            phone_number,
            expected_status_code,
            send_sms,
            client
    ):
        url = reverse('login_step_1_view')
        data = {"phone_number": phone_number} if phone_number is not None else {}

        with mock.patch.object(models.Model, 'save'):
            response = client.post(url, data)
            assert response.status_code == expected_status_code

        if send_sms:
            send_verification_sms_mock.assert_called_once()
        else:
            send_verification_sms_mock.assert_not_called()
