from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv

load_dotenv()


def send_mail_function(email, context):
    mesg = context.get("message")
    title = context.get("title")
    msg = EmailMultiAlternatives(
        f"{title}",
        f"{mesg}!",
        os.environ.get("EMAIL_HOST_USER", "kingshahi163@gmail.com"),
        [email],
    )
    email_html_message = render_to_string("email.html", context)
    msg.attach_alternative(email_html_message, "text/html")
    msg.send(fail_silently=True)
