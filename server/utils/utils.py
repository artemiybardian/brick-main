# users/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import tokens
from django.utils.encoding import smart_bytes


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


class Util:
    @staticmethod
    def send(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()


class PasswordReset:
    @staticmethod
    def send_email(user, request):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = tokens.PasswordResetTokenGenerator().make_token(user)

        doamin = get_current_site(request).domain

        path = reverse(
            "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        redirect_url = settings.FRONTEND_URL + "/reset-password-complete"
        url = "http://{}{}?redirect_url={}".format(doamin, path, redirect_url)

        body = 'Здравствуйте! Вы можете воспользоваться ссылкой ниже, чтобы сбросить пароль на "CyberDoc":\n{}'.format(
            url
        )
        data = {
            "email_subject": "Сбросьте свой пароль",
            "email_body": body,
            "to_email": user.email,
        }

        Util.send(data)