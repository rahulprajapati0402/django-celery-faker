import random
from .models import Student


from faker import Faker

fake = Faker()


def seed_db(n):
    for i in range(0, n):
        Student.objects.create(name=fake.name(), age=random.randint(20, 50))
