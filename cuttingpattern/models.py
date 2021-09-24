from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class CustomerGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    group = models.ForeignKey(CustomerGroup, blank=True, null=True, related_name="childs", on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

class CuttingPattern(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.TextField()
    description = models.TextField()
    machine_code = models.TextField()
    json_file = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name="cuttingpatterns", on_delete=DO_NOTHING)
    created  = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, related_name="cuttingpatterns", on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.file_name} - {self.description}"