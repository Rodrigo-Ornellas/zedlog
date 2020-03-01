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


class Vessels(models.Model):
    # vname = models.CharField(max_length=30, null=True, blank=True)
    vcode = models.CharField(max_length=30)
    voyage = models.IntegerField()
    saleDate = models.DateField(null=True, blank=True)  # Data when SHIP will leave port
    checkedDate = models.DateTimeField(auto_now_add=True)  # Checks Confirmed Date
    checkID = models.IntegerField()
    vcolor = models.CharField(max_length=255)

    def __str__(self):
        return ('%s %s %s' % (self.pk, self.vcode, self.voyage))


class PortName(models.Model):
    pname = models.CharField(max_length=30, null=True, blank=True)
    pcode = models.CharField(max_length=30)

    def __str__(self):
        return ('%s' % (self.pcode))


class Containers(models.Model):
    # INVENTORY OF CONTAINERS    
    # CONTAINER_STATUS = (
    #     ('0', 'Active'),
    #     ('1', 'Damaged'),
    #     ('2', 'Lost'),
    #     ('3', 'Painting'),
    #     ('4', 'Inactive'),
    # )
    # CONTAINER_TYPES = (
    #     ('0', '40GP96'),
    #     ('1', '20GP86'),
    #     ('2', '20TD86'),
    #     ('3', '40GP96'),
    # )
    # status        = models.CharField(max_length=20, choices=CONTAINER_STATUS, default='Active')
    # leftTo        = models.ForeignKey(PortName, on_delete=models.SET(1))    
    status        = models.CharField(max_length=20, default='Active')
    containerID   = models.CharField(max_length=32)
    ctype         = models.CharField(max_length=32) #, choices=CONTAINER_TYPES)
    leftTo        = models.ForeignKey(PortName, on_delete=models.CASCADE)
    isActive      = models.BooleanField(default=True)
    # registerDate  = models.DateField(auto_now_add=True)

    def __str__(self):
        return ('%s - %s' % (self.containerID, self.isActive))


# class Trips(models.Model):
#     uploadDate = models.DateTimeField(auto_now_add=True)
#     vessel = models.ForeignKey(Vessels, on_delete=models.SET(1))
#     containerID = models.ForeignKey(Containers, on_delete=models.SET(1))
#     voyageID = models.DecimalField(decimal_places=0, max_digits=1000)
#     saleDate = models.DateField()  # Data when SHIP will leave port
#     checkedDate = models.DateField()  # Checks Confirmed Date
#     isFinalCheck = models.BooleanField(default=False)

#     pod = models.ForeignKey(PortName, on_delete=models.SET(1))
#     location = models.CharField(max_length=10)
#     position = models.CharField(max_length=20)
#     booking = models.CharField(max_length=20)
#     peso = models.DecimalField(decimal_places=2, max_digits=20)
#     carga = models.DecimalField(decimal_places=2, max_digits=20)
#     arrival = models.CharField(max_length=50, null=True, blank=True)
#     onhold = models.CharField(max_length=20, null=True, blank=True)
#     commodity = models.CharField(max_length=50, null=True, blank=True)
#     haz = models.CharField(max_length=50, null=True, blank=True)
#     reefer = models.CharField(max_length=10, null=True, blank=True)
#     ondock = models.CharField(max_length=1, null=True, blank=True)
#     oog = models.CharField(max_length=50, null=True, blank=True)

#     def __str__(self):
#         return ('%s - %s - %s - %s' % (self.vessel, self.voyageID, self.pod, self.booking))



class PortData(models.Model):
    filefk     = models.ForeignKey(PortFILE, on_delete=models.CASCADE, null=True)
    vessel     = models.ForeignKey(Vessels, on_delete=models.CASCADE, null=True)    
    serial     = models.CharField(max_length=15, null=True, blank=True)
    tipo       = models.CharField(max_length=10, null=True, blank=True)
    location   = models.CharField(max_length=10, null=True, blank=True)
    full       = models.CharField(max_length=10, null=True, blank=True)
    pod        = models.ForeignKey(PortName, on_delete=models.SET(1))
    position   = models.CharField(max_length=20, null=True, blank=True)
    booking    = models.CharField(max_length=20, null=True, blank=True)
    peso       = models.DecimalField(decimal_places=2, max_digits=20)
    carga      = models.DecimalField(decimal_places=2, max_digits=20)
    arrival    = models.CharField(max_length=50, null=True, blank=True)
    onhold     = models.CharField(max_length=20, null=True, blank=True)
    commodity  = models.CharField(max_length=50, null=True, blank=True)
    haz        = models.CharField(max_length=50, null=True, blank=True)
    reefer     = models.CharField(max_length=10, null=True, blank=True)
    ondock     = models.CharField(max_length=1, null=True, blank=True)
    oog        = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return ('%s - %s - %s - %s - %s' % (self.serial, self.tipo, self.pod, self.booking))

    # '%d-%m-%Y %H:%M:%S'
    # 11-16-2018 10:58:53 PM
    #  YYYY-MM-DD HH:MM
    # arrival = models.RodsDTField(blank=True, null=True)
    # arrival = models.DateTimeField(blank=True, null=True)
    # ondock = models.BooleanField()

