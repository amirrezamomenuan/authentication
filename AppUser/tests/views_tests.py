from types import SimpleNamespace
from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status
from django.db import models

from AppUser.models import LoginRequest, AppUser
from AppUser.token_generator import JWTTokenGenerator


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


class TestLoginViewStep2:
    @pytest.mark.parametrize(
        'verification_data', [
            {'phone_number': '09123456789'},
            {'verification_code': '45189'},
            {}
        ]
    )
    @mock.patch.object(LoginRequest, 'get_last_valid_request')
    def test_with_giving_incomplete_data_should_fail(
            self,
            login_request_mock,
            verification_data,
            client
    ):
        url = reverse('login_step_2_view')
        response = client.post(url, verification_data)

        login_request_mock.assert_not_called()
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    @mock.patch.object(LoginRequest, 'get_last_valid_request')
    @mock.patch.object(AppUser.objects, 'update_or_create')
    @mock.patch.object(JWTTokenGenerator, 'generate_token_pair')
    def test_with_giving_valid_phone_number_and_verification_code_should_pass(
            self,
            token_generator_mock,
            app_user_mock,
            validation_mock,
            client,
            login_request
    ):
        url = reverse('login_step_2_view')
        data = {
            'phone_number': '09123456789',
            'verification_code': '45189'
        }

        user = SimpleNamespace(id=123)
        app_user_mock.return_value = (user, True)
        token_generator_mock.return_value = {"refresh_token": '1dfslk1r', "access_token": '541fcv2'}
        validation_mock.return_value = login_request

        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        app_user_mock.assert_called_once()
        token_generator_mock.assert_called_once()

    @mock.patch.object(LoginRequest, 'get_last_valid_request', return_value=None)
    def test_with_giving_invalid_phone_number_and_verification_code_should_fail(
            self,
            get_last_valid_request_mock,
            client,
    ):
        url = reverse('login_step_2_view')
        data = {
            'phone_number': '09123456789',
            'verification_code': '45189'
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetAccessTokenView:
    def test_getting_access_token_without_providing_refresh_token(self, client):
        url = reverse('access_token_view')
        response = client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        'access_token, is_valid, expected_status_code', [
            ('valid.access.token1234', True, status.HTTP_200_OK),
            (None, False, status.HTTP_400_BAD_REQUEST)
        ]
    )
    def test_getting_access_token_with_different_refresh_tokens(
            self,
            access_token,
            is_valid,
            expected_status_code,
            client
    ):
        with mock.patch('AppUser.views.JWTTokenGenerator.generate_access_token') as tg:
            tg.return_value = access_token
            url = reverse('access_token_view')
            response = client.post(url, {"refresh_token": 'some_valid_refresh_token'})
            assert response.status_code == expected_status_code
