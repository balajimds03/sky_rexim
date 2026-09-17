import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import traceback
from django.core.mail import send_mail
from django.conf import settings

try:
    print(f"Sending test email from {settings.EMAIL_HOST_USER} to {settings.EMAIL_HOST_USER}...")
    send_mail(
        'Test Subject',
        'Test Message',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print('SUCCESS: Email sent successfully!')
except Exception as e:
    print('ERROR: Failed to send email.')
    traceback.print_exc()
