import time

from celery import shared_task

@shared_task()
def send_verification_sms(phone_number: str, verification_code: str):
    time.sleep(5)
    sms_text = f'verification code for {phone_number}: {verification_code}'
    print(sms_text)
