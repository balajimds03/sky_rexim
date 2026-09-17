import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.test import RequestFactory
from accounts.views import ForgotPasswordRequest
from accounts.models import User
import json

# Create a dummy user for testing
email = "jayabalaji2003kdm@gmail.com"
if not User.objects.filter(email=email).exists():
    # Attempt to create or fetch a user
    print(f"User with email {email} does not exist in DB. Creating one for test...")
    # we need username
    try:
        User.objects.create(email=email, username="testuser123", password="123")
    except Exception as e:
        print("Could not create user:", e)
        # Maybe username exists?

factory = RequestFactory()
request = factory.post('/fake-url/', data=json.dumps({"email": email}), content_type='application/json')

view = ForgotPasswordRequest.as_view()
try:
    response = view(request)
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.data)
except Exception as e:
    import traceback
    print("Exception occurred:")
    traceback.print_exc()
