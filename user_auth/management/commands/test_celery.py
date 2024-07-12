from django.core.management.base import BaseCommand
from user_auth.tasks import generate_account_number_and_otp

class Command(BaseCommand):
    help = 'Test Celery Task'

    def handle(self, *args, **kwargs):
        result = generate_account_number_and_otp.delay('otp_num')
        print(f'Task Result: {result}')
        print('Task queued successfully')
