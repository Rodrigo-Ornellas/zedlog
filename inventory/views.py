from django.shortcuts import render
from .models import Containers
from django.contrib.auth.decorators import permission_required, login_required

def CheckContainer(serial, ctype, pdest):
    # > working OK!
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the CONTAINER data already exists in the database
    # returns either '' or CONTAINER ID (for Foreign Key)
    # =============================================
    try:
        # print("serial > {}".format(serial))
        # print("ctype > {}".format(ctype))
        # print("pdest > {}".format(pdest))        
        container = Containers.objects.get(serial=serial)
    except:
        print('failed! > 1 - CheckContainer')
        try:
            container, created = Containers.objects.update_or_create(serial=serial, ctype=ctype, pod=pdest)
            container.save()
        except:
            print('failed! > 2 - CheckContainer <<<<<<')

    return container


@login_required(login_url='login')
def listInventory(request):
    # > working OK!
    # =============================================
    # this VIEW lists all vessels
    # =============================================    
    data = {}
    data['containers'] = Containers.objects.all()
    return render(request, 'inventory/contaniers.html', data)
