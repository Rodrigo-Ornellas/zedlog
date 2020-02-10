from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SchedFILE(models.Model):
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now_add=True)
    filename = models.FileField()
