from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.


# class RodsDTField(models.DateTimeField):
#     # https://stackoverflow.com/questions/8172041/passing-date-time-in-a-different-format-to-models-datetimefield-in-django
#     def get_prep_value(self, value):
#         return str(datetime.strptime(value, "%d-%m-%Y %H:%M:%S"))
# uploaded_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
# uploaded_by = models.ForeignKey( get_user_model(), on_delete=models.CASCADE, )
# uploaded_by = models.ForeignKey( User, on_delete=models.CASCADE, )

class PortFILE(models.Model):
    # uploaded_by is NOT working
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    filename = models.FileField(upload_to='port/')


def __str__(self):
    return self.filename


class PortCSV(models.Model):
    filefk = models.ForeignKey(
        PortFILE, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    serial = models.CharField(max_length=15, null=True, blank=True)
    tipo = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=10, null=True, blank=True)
    full = models.CharField(max_length=10, null=True, blank=True)
    pod = models.CharField(max_length=10, null=True, blank=True)
    position = models.CharField(max_length=20, null=True, blank=True)
    booking = models.CharField(max_length=20, null=True, blank=True)
    vessel = models.CharField(max_length=10, null=True, blank=True)
    peso = models.DecimalField(decimal_places=2, max_digits=20)
    carga = models.DecimalField(decimal_places=2, max_digits=20)
    arrival = models.CharField(max_length=50, null=True, blank=True)
    onhold = models.CharField(max_length=20, null=True, blank=True)
    commodity = models.CharField(max_length=50, null=True, blank=True)
    haz = models.CharField(max_length=50, null=True, blank=True)
    reefer = models.CharField(max_length=10, null=True, blank=True)
    ondock = models.CharField(max_length=1, null=True, blank=True)
    oog = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return ('%s - %s - %s - %s' % (self.serial, self.tipo, self.pod, self.booking))

    # '%d-%m-%Y %H:%M:%S'
    # 11-16-2018 10:58:53 PM
    #  YYYY-MM-DD HH:MM
    # arrival = models.RodsDTField(blank=True, null=True)
    # arrival = models.DateTimeField(blank=True, null=True)
    # ondock = models.BooleanField()
