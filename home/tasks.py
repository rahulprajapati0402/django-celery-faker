import time
import uuid
import os
import pandas as pd
from celery import shared_task
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
