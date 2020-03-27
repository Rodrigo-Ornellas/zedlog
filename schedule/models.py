from django.db import models
from django.contrib.auth.models import User


class SchedFILE(models.Model):
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now_add=True)
    fnamePDF = models.FileField()
    fnameCSV = models.FileField()

    def __str__(self):
        return self.filename


class Vessels(models.Model):
    # This MODEL represnts the SHIPS or VESSELS that are being PROCESSED
    vnameA          = models.CharField(max_length=30)
    vnameB          = models.CharField(max_length=30, null=True, blank=True)
    description     = models.CharField(max_length=30, null=True, blank=True)
    portName        = models.CharField(max_length=30, default="deltaport")
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
        return ('%s - %s - %s - %s' % (self.pk, self.vnameA, self.vnameB, self.portName))

