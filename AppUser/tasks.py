import time
import logging

from django.conf import settings
import requests
from celery import shared_task

logger = logging.getLogger('otp')


@shared_task()
def send_verification_sms(phone_number: str, verification_code: str):
    if True:  # since I cannot charge otp right now, I am printing the verification code for ease
        time.sleep(5)
        sms_text = f'verification code for {phone_number}: {verification_code}'
        print(sms_text)

    data = {
        'phone_number': phone_number,
        'message': f'uber-clone verificatoin code : {verification_code}'
    }
    headers = {
        'OTP-Secret-Token': settings.OTP_SECRET_TOKEN
    }

    try:
        response = requests.post(
            url=settings.OTP_VERIFICATION_SMS_URL,
            json=data,
            headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(
            '[sending sms failed]-[phone_number: {}]-[error: {}]'.format(
                phone_number,
                e,
            )
        )

