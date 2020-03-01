#!/usr/bin/python
# -*- coding: latin-1 -*-

from django.contrib import admin
from valdata.views import PORTFL_ListFiles, PORTFL_Upload, graph, index, PORTFL_Del, message, PORTDT_ListData, vsldash, ListVessels
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from schedule.views import downloadSched

urlpatterns = [
    path('', index, name='urlindex'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portfiles/', PORTFL_ListFiles, name='urlportfiles'),
    path('csvupload/', PORTFL_Upload, name='urlcsvupload'),
    path('csvdata/', PORTDT_ListData, name='urlcsvdata'),
    path('graph/', graph, name='urlgraph'),
    path('portfiles/delete/<int:id>', PORTFL_Del, name='urldeletefile'),
    path('schedule/update', downloadSched, name='urlscheduleget'),
    path('msg/<str:msg>', message, name='urlmessage'),
    path('vsldash/<int:trip>/<int:ver>', vsldash, name='urlvsldash'),
    path('vsllist/', ListVessels, name='urlvsllist'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
