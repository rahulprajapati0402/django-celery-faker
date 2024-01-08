from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import time
from celery.result import AsyncResult
from .tasks import handle_sleep, export_student_excel, send_mail_to_all
from django.contrib.auth.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
import uuid


# Create your views here.


def home(request):
    # time.sleep(10)
    data = handle_sleep.delay()
    return HttpResponseRedirect(data.task_id)


def generate_excel(request):
    export_student_excel.delay()
    return HttpResponse("Excel will be generated soon.")


def check_status(request, task_id):
    response = AsyncResult(task_id)
    print(response.ready())
    return HttpResponse(response.ready())


def send_email_to_users(request):
    send_mail_to_all.delay()
    return HttpResponse("Email sent successfully!")


def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour=11, minute=57)
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name=f"schedule_mail_task_{str(uuid.uuid4())}",
        task="home.tasks.send_mail_to_all",
        # args=json.dumps([[2, 3]]),
    )
    return HttpResponse("Done")
