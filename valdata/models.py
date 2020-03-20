from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class PortFILE(models.Model):
    # This MODEL represents the PORTDATA files that are being uploaded
    uploaded_by     = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date            = models.DateTimeField(auto_now_add=True)
    filename        = models.FileField(upload_to='port/')

    def __str__(self):
        return self.filename

class PortName(models.Model):
    # This MODEL represents the POD or Ports of Destination
    pname       = models.CharField(max_length=30, null=True, blank=True)
    pcode       = models.CharField(max_length=30)

    def __str__(self):
        return ('%s' % (self.pcode))


class Vessels(models.Model):
    # This MODEL represnts the SHIPS or VESSELS that are being PROCESSED
    vslfull         = models.CharField(max_length=30)
    portName        = models.CharField(max_length=30)
    vcode           = models.CharField(max_length=30)
    vname           = models.CharField(max_length=30, null=True, blank=True)
    voyage          = models.IntegerField()
    line            = models.CharField(max_length=5)
    service         = models.CharField(max_length=5)
    erdDate         = models.DateTimeField(null=True, blank=True) 
    cutoffDate      = models.DateTimeField(null=True, blank=True) # last date for container to arrive to port
    demurrageRFT    = models.DateField(null=True, blank=True) # Date when is not charged
    shipETAdate     = models.DateField(null=True, blank=True) # Date ship will arrive to port
    shipETAtime     = models.CharField(max_length=10, null=True, blank=True) # Time ship will arrive to port or COMPLETED when ship left port
    shipETDdate     = models.DateTimeField(null=True, blank=True)  # Date when SHIP will leave port
    checkedDate     = models.DateTimeField(auto_now_add=True)  # Checks Confirmed Date

    def __str__(self):
        return ('%s - %s - %s' % (self.pk, self.vcode, self.voyage))


class Containers(models.Model):
    # This MODEL registers new CONTAINERS for an Inventory of Containers
    serial        = models.CharField(max_length=32)
    ctype         = models.CharField(max_length=32)
    pod           = models.ForeignKey(PortName, on_delete=models.CASCADE)
    isActive      = models.BooleanField(default=True)
    lastUpdate    = models.DateField(auto_now_add=True)

    def __str__(self):
        return ('%s' % (self.containerID))


class PortData(models.Model):
    # This MODEL represents each UPLOAD of DATA to be processed
    filefk     = models.ForeignKey(PortFILE, on_delete=models.CASCADE, null=True)
    vessel     = models.ForeignKey(Vessels, on_delete=models.CASCADE, null=True)    
    serial     = models.ForeignKey(Containers, on_delete=models.CASCADE, null=True)
    tipo       = models.CharField(max_length=10, null=True, blank=True)
    location   = models.CharField(max_length=10, null=True, blank=True)
    full       = models.CharField(max_length=10, null=True, blank=True)
    pod        = models.ForeignKey(PortName, on_delete=models.SET(1))
    position   = models.CharField(max_length=20, null=True, blank=True)
    booking    = models.CharField(max_length=20, null=True, blank=True)
    peso       = models.DecimalField(decimal_places=2, max_digits=20)
    carga      = models.DecimalField(decimal_places=2, max_digits=20)
    arrival    = models.DateTimeField(max_length=50, null=True, blank=True)
    onhold     = models.CharField(max_length=20, null=True, blank=True)
    commodity  = models.CharField(max_length=50, null=True, blank=True)
    haz        = models.CharField(max_length=50, null=True, blank=True)
    reefer     = models.CharField(max_length=10, null=True, blank=True)
    ondock     = models.CharField(max_length=1, null=True, blank=True)
    oog        = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return ('%s - %s - %s - %s' % (self.serial, self.tipo, self.pod, self.booking))

class VesselPortData(models.Model):
    # This MODEL JOINS Vessels Table with the many uploads of PORTDATA
    vsl         = models.ForeignKey(Vessels, on_delete=models.CASCADE, null=True)
    prtdt       = models.ForeignKey(PortData, on_delete=models.CASCADE, null=True)
    version     = models.IntegerField(blank=True, null=True) # version of the uploaded vessels
    vcolor      = models.CharField(max_length=255)    
