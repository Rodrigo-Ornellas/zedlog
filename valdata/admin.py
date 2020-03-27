from django.contrib import admin

from .models import PortFILE, PortData #, Vessels, PortName, Containers

admin.site.register(PortFILE)
admin.site.register(PortData)
# admin.site.register(PortName)
# admin.site.register(Vessels)
# admin.site.register(Containers)

