from django.shortcuts import render
from .models import PortRegistry

from django.contrib.auth.decorators import permission_required, login_required

def CheckPort(code):
    # > working OK!
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================
    try:
        # print("CHECKPORT input > ", code);
        port = PortRegistry.objects.get(portName=code)
        # print("CHECKPORT port > ", port);
    except:
        print('failed! > 1 - CheckPort')
        try:
            port = PortRegistry(portName=code)
            port.save()
        except:
            print('failed! > 2 - CheckPort')

    return port


def CheckAgent(code):
    # > working OK!
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================
    try:
        agent = PortRegistry.objects.get(agentName=code)
    except:
        print('failed! > 1 - CheckAgent')
        try:
            agent = PortRegistry(agentName=code)
            agent.save()
        except:
            print('failed! > 2 - CheckAgent')

    return agent, agent.agentName    


@login_required(login_url='login')
def listPorts(request):
    # > working OK!
    # =============================================
    # this VIEW lists all vessels
    # =============================================    
    data = {}
    data['ports'] = PortRegistry.objects.all()
    return render(request, 'portname/portnames.html', data)