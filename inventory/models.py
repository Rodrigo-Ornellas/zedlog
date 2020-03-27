from django.db import models
from portname.models import PortRegistry

class Containers(models.Model):
    # This MODEL registers new CONTAINERS for an Inventory of Containers
    serial        = models.CharField(max_length=32)
    ctype         = models.CharField(max_length=32)
    pod           = models.ForeignKey(PortRegistry, on_delete=models.CASCADE)
    isActive      = models.BooleanField(default=True)
    lastUpdate    = models.DateField(auto_now_add=True)

    def __str__(self):
        return ('%s - %s' % (self.pk, self.serial))
