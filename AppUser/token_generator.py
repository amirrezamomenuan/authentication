import jwt
from jwt import ExpiredSignatureError, DecodeError, InvalidSignatureError

from django.conf import settings
from django.utils import timezone


class JWTTokenGenerator:
    """
    this class is used for generating access_token
    and token pair (access & refresh).
    generating a refresh token directly is not possible
    """

    @staticmethod
    def __generate_token(payload: dict):
        return jwt.encode(
            payload=payload,
            key=settings.JWT_AUTHENTICATION_KEY,
            algorithm='HS256'
        )

    @classmethod
    def __generate_refresh_token(cls, user_id: int):
        payload = dict()
        payload['uid'] = user_id
        payload['exp'] = timezone.now() + timezone.timedelta(seconds=settings.REFRESH_TOKEN_EXPIRATION_TIME)

        return cls.__generate_token(payload=payload)

    @classmethod
    def generate_access_token(
            cls,
            refresh_token: str
    ):
        """
        this method receives a refresh token in string form
        and creates an access token from its extracted data
        """
        payload = dict()

        try:
            decoded_data = jwt.decode(
                refresh_token,
                settings.JWT_AUTHENTICATION_KEY,
                ['HS256']
            )
            payload['uid'] = decoded_data.get('user_id')
            payload['exp'] = timezone.now() + timezone.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRATION_TIME)
        except (ExpiredSignatureError, DecodeError, InvalidSignatureError):
            return None

        return cls.__generate_token(payload=payload)

    @classmethod
    def generate_token_pair(cls, user_id: int) -> dict:
        refresh_token = cls.__generate_refresh_token(user_id=user_id)
        access_token = cls.generate_access_token(refresh_token=refresh_token)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
