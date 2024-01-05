import time
import uuid
import os
import pandas as pd
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Student


@shared_task
def handle_sleep():
    print("Handle sleep started")
    time.sleep(10)


@shared_task
def export_student_excel():
    students = Student.objects.all()
    df = pd.DataFrame(list(students))
    file_path = os.path.join(settings.BASE_DIR, f"{uuid.uuid4()}.csv")
    df.to_csv(file_path, encoding="UTF-8")


@shared_task
def send_mail_to_all():
    users = User.objects.filter(email__isnull=False).exclude(email="")
    for user in users:
        subject = "Django Celery Learning"
        message = "I am learning celery in django."
        to_user = [user.email]
        send_mail(
            subject=subject,
            message=message,
            recipient_list=to_user,
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False,
        )
