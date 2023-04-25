
# TODO : this should be a celery @shared_task
def send_verification_sms(phone_number: str, verification_code: str):
    sms_text = f'your verification code\n {verification_code}'
    print(sms_text)