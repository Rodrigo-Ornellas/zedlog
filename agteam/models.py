from django.db import models
from django.contrib.auth.models import User

from schedule.models import Vessels
from inventory.models import Containers
from portname.models import PortRegistry


class AgentFILE(models.Model):
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now_add=True)
    filename = models.FileField()

    def __str__(self):
        return self.filename

class VAConnector(models.Model):
    # This MODEL JOINS Vessels Table with the many uploads of PORTDATA
    vsl         = models.ForeignKey(Vessels, on_delete=models.CASCADE, null=True)
    version     = models.IntegerField(blank=True, null=True) # version of the uploaded vessels
    vcolor      = models.CharField(max_length=255)

    def __str__(self):
        return ('%s - %s' % (self.vsl.vslfull,  self.version))


class AgentData(models.Model):
    # This MODEL represents each UPLOAD of DATA to be processed
    filefk     = models.ForeignKey(AgentFILE, on_delete=models.CASCADE)
    vessel     = models.ForeignKey(Vessels, on_delete=models.CASCADE)    
    connector  = models.ForeignKey(VAConnector, on_delete=models.CASCADE)
    serial     = models.ForeignKey(Containers, on_delete=models.CASCADE, null=True)
    tipo       = models.CharField(max_length=10, null=True, blank=True)
    location   = models.CharField(max_length=10, null=True, blank=True)
    full       = models.CharField(max_length=10, null=True, blank=True)
    pod        = models.ForeignKey(PortRegistry, on_delete=models.SET(1))
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