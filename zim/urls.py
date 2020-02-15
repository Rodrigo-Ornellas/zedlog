from django.urls import path, include
from django.contrib import admin
from valdata.views import portFILES, csvupload, graph, index, deleteFile, message, csvdata
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from schedule.views import downloadSched

urlpatterns = [
    path('', index, name='urlindex'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portfiles/', portFILES, name='urlportfiles'),
    path('csvupload/', csvupload, name='urlcsvupload'),
    path('csvdata/', csvdata, name='urlcsvdata'),
    path('graph/', graph, name='urlgraph'),
    path('portfiles/delete/<int:id>', deleteFile, name='urldeletefile'),
    path('schedule/update', downloadSched, name='urlscheduleget'),
    path('msg/<str:msg>', message, name='urlmessage'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
