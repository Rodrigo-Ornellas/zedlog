from django.db import models


class PortRegistry(models.Model):
    # This MODEL represents the POD or Ports of Destination
    portName    = models.CharField(max_length=30, null=True, blank=True)
    agentName   = models.CharField(max_length=30, null=True, blank=True)
    fullName    = models.CharField(max_length=30, null=True, blank=True)
    country     = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        if ( self.agentName != ''):
            return ('%s - %s' % (self.portName, self.agentName))
        else:
            return ('%s' % (self.portName))


