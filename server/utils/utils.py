# users/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

def send_verification_email(user, request):
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.auth.tokens import default_token_generator

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    current_site = "127.0.0.1:8000"
    activation_link = f"http://127.0.0.1:8000/api/verify-email/{uid}/{token}/"

    send_mail(
        subject="Подтверждение по электронной почте",
        message=f"Уважаемый пользователь, нажмите на ссылку ниже, чтобы подтвердить свой адрес электронной почты: {activation_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
