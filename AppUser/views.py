from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import LoginRequest, AppUser
from .utils import send_verification_sms
from .authentication import JWTTokenGenerator

class LoginView(ViewSet):
    def login_step_1(self, request):
        try:
            phone_number = str(request.data.get('phone_number'))
        except (TypeError, ValueError):
            return Response(
                data={'message': 'invalid phone number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            login_request = LoginRequest(phone_number=phone_number)
            login_request.save()
        except ValidationError as error_message:
            return Response(
                data={'message': dict(error_message).values()},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_verification_sms(
            phone_number=phone_number,
            verification_code=login_request.verification_code
        )

        return Response(
            data={"message": 'verification code sent'},
            status=status.HTTP_201_CREATED
        )

    def login_step_2(self, request):
        try:
            phone_number = str(request.data.get('phone_number'))
            verification_code = str(request.data.get('verification_code'))
        except (TypeError, ValueError):
            return Response(
                data={'message': 'invalid data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        code_verified = LoginRequest.validate_verification_code(
            phone_number=phone_number,
            verification_code=verification_code
        )
        if code_verified:
            app_user, _ = AppUser.objects.update_or_create(
                phone_number=phone_number,
                defaults={}
            )
            
            token_pair = JWTTokenGenerator.generate_token_pair(
                user_id=app_user.id
            )

            return Response(data=token_pair)

        else:
            return Response(
                data={'message': 'invalid verification code'},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetAccessTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = str(request.data.get('refresh_token'))
        except (TypeError, ValueError):
            return Response(
                data={'message': 'invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        access_token = JWTTokenGenerator.generate_access_token(refresh_token)

        return Response(
            data={"access_token": access_token},
        )