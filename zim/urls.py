from django.contrib import admin
from valdata.views import PORTFL_ListFiles, PORTFL_Upload, index, PORTFL_Del, message, PORTDT_ListData, vsldash, ListVessels, ListContainers, Demurrage, listSchedule
from schedule.views import saveSchedule

from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='urlindex'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portfiles/', PORTFL_ListFiles, name='urlportfiles'),
    path('csvupload/', PORTFL_Upload, name='urlcsvupload'),
    path('csvdata/', PORTDT_ListData, name='urlcsvdata'),
    path('portfiles/delete/<int:id>', PORTFL_Del, name='urldeletefile'),
    path('msg/<str:msg>', message, name='urlmessage'),
    path('vsldash/<int:trip>/<int:ver>', vsldash, name='urlvsldash'),
    path('vsllist/', ListVessels, name='urlvsllist'),
    path('contlist/<int:trip>/<int:ver>', ListContainers, name='urlcontlist'),
    path('demurrage/<str:choice>/<int:trip>/<int:ver>', Demurrage , name='urldemurrage'),
    path('schedule/update', saveSchedule, name='urlscheduleget'),
    path('schedule/list', listSchedule, name='urllistschedule')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
