from django.contrib import admin
from valdata.views import PORTFL_ListFiles, PORTFL_Upload, index, PORTFL_Del, message, PORTDT_ListData
from dashboard.views import vsldash, ListContainers, Demurrage
from schedule.views import saveSchedule, delSchedule, filesSchedule, listSchedule#, ListVessels
from inventory.views import listInventory
from portname.views import listPorts

from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='urlindex'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portfiles/', PORTFL_ListFiles, name='urlportfiles'),
    path('portfiles/delete/<int:id>', PORTFL_Del, name='urldeletefile'),
    path('csvupload/', PORTFL_Upload, name='urlcsvupload'),
    path('csvdata/', PORTDT_ListData, name='urlcsvdata'),
    path('msg/<str:msg>', message, name='urlmessage'),
    path('vsldash/<int:trip>/<int:ver>', vsldash, name='urlvsldash'),
    # path('vsllist/', ListVessels, name='urlvsllist'),
    path('contlist/<int:trip>/<int:ver>', ListContainers, name='urlcontlist'),
    path('demurrage/<str:choice>/<int:trip>/<int:ver>', Demurrage , name='urldemurrage'),
    path('schedule/update', saveSchedule, name='urlscheduleget'),
    path('schedule/list', listSchedule, name='urllistschedule'),
    path('schedule/del/<int:id>', delSchedule, name='urldelschedule'),
    path('schedule/files', filesSchedule, name='urlfilesschedule'),
    path('inventory/list', listInventory, name='urllistinventory'),
    path('portname/list', listPorts, name='urllistports')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
