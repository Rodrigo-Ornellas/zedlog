from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render

from valdata.models import PortData
from schedule.models import Vessels

from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q




def DemurrageList(choice, trip, ver):
    # FILTERING THE CONTAINERS IN THE PORT COLLECTING DEMURRAGE
    # SELECT * FROM valdata_portdata WHERE vessel_id=12 AND reefer <> '';
    # hoje = datetime.now()
    hoje = datetime.strptime('02-29-2020 12:00:00', '%m-%d-%Y %H:%M:%S')
    print(hoje)
    days7_week = datetime.now()-timedelta(days=7)
    days15_warning = datetime.now()-timedelta(days=15)
    days_critical = datetime.now()-timedelta(days=720)

    if choice == "critical":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).filter(arrival__range=[days_critical, days15_warning])

    if choice == "weekold":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).filter(arrival__range=[days7_week, hoje])

    if choice == "warning":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).filter(arrival__range=[days15_warning, days7_week])

    if choice == "notarrived":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).filter(arrival__contains='- - -')

    if choice == "hazmaterial":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).exclude(haz=u'')

    if choice == "reefer":
        return PortData.objects.filter(vessel__voyage=trip).filter(version=ver).exclude(reefer=u'')
    


@login_required(login_url='login')
def Demurrage(request, choice, trip, ver):
    # =============================================
    # this VIEW updates the SAIL date of the vessel
    # 
    # =============================================

    data = {}
    data['container'] = DemurrageList(choice, trip, ver)
    data['choice'] = choice
    data['header'] = "Demurrage"
    return render(request, 'dashboard/contlist.html', data)


# @login_required(login_url='login')
# def vslSailDate(request, trip, ver, sdate):
#     # =============================================
#     # this VIEW updates the SAIL date of the vessel
#     # 
#     # =============================================
#     sailDate = Vessels.objects.filter(voyage=trip).update(shipETDdate=sdate)


@login_required(login_url='login')
def vsldash(request, trip, ver):
    # =============================================
    # this VIEW shows a DASHBOARD of the 
    # PORTDATA that has been uploaded
    # =============================================
    data = {}

    # Getting the number of Bookings on this Vessel
    bookings = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).aggregate(Count('booking', distinct=True))

    # Getting the number of Containers on this Vessel
    containers = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).aggregate(Count('serial', distinct=True))

    # Adding the total weight of the Containers and Cargo
    tweight = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).aggregate(total_weights=Sum('peso'))

    # Adding the total weight of the Containers and Cargo
    cweight = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).aggregate(total_weights=Sum('carga'))

    # Adding the total weight of the Containers and Cargo
    vdata = PortData.objects.filter(vessel__voyage=trip).filter(version=ver)

    # Summary of Container Type Data for the PIE Graph
    # GRAPH 1
    ctype = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).values('tipo').annotate(c=Count('tipo')).order_by('-c')
    typeKey = []
    typeValue = []
    typeTotal = 0
    # Build data for Chart.JS build the graph
    for k in ctype:
        typeKey.append(k["tipo"])
        typeValue.append(k["c"])
        typeTotal += k["c"]


    #  POD or Port of Destination Data for BAR Graph
    # GRAPH 2
    gpod = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).values('pod__pcode').annotate(c=Count('pod')).order_by('-c')
    podKey = []
    podValue = []
    podTotal = 0
    # Build data for Chart.JS build the graph
    for k in gpod:
        podKey.append(k["pod__pcode"])
        podValue.append(k["c"])
        podTotal += k["c"]


    #  LOCATION or Transport Modal for PIE Graph
    # GRAPH 3
    location = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).values('location').annotate(c=Count('location')).order_by('-c')
    locKey = []
    locValue = []
    locTotal = 0
    # Build data for Chart.JS build the graph
    for k in location:
        locKey.append(k["location"])
        locValue.append(k["c"])
        locTotal += k["c"]


    # If there ARE ships
    if tweight['total_weights'] is not None:
        data['vessel'] = Vessels.objects.get(voyage=trip, vpdconnector__version=ver).vcode
        data['bookings'] = bookings
        data['containers'] = containers
        data['voyage'] = trip
        data['typeKey'] = typeKey
        data['typeValue'] = typeValue
        data['podKey'] = podKey
        data['podValue'] = podValue
        data['locKey'] = locKey
        data['locValue'] = locValue        
        data['color'] = Vessels.objects.get(voyage=trip, vpdconnector__version=ver).vcolor
        data['version'] = ver
        data['tweight'] = "{:,}".format(int(tweight['total_weights']/1000)) 
        data['cweight'] = "{:,}".format(int(cweight['total_weights']/1000)) 
        data['weekoldCount'] = DemurrageList("weekold", trip, ver).aggregate(Count('serial', distinct=True))
        data['warningCount'] = DemurrageList("warning", trip, ver).aggregate(Count('serial', distinct=True))
        data['criticalCount'] = DemurrageList("critical", trip, ver).aggregate(Count('serial', distinct=True))
        data['notarrivedCount'] = DemurrageList("notarrived", trip, ver).aggregate(Count('serial', distinct=True))
        data['hazmaterialCount'] = DemurrageList("hazmaterial", trip, ver).aggregate(Count('serial', distinct=True))
        data['reeferCount'] = DemurrageList("reefer", trip, ver).aggregate(Count('serial', distinct=True))
        

        template = "dashboard/vsldash.html"
        return render(request, template, data)
    
    # If there AREN'T any SHIPS
    else:
        return redirect('urlmessage', msg='No data available for this ship.')



@login_required(login_url='login')
def ListContainers(request, trip, ver):
    # =============================================
    # this VIEW lists all the trips
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================    
    data = {}
    data['user'] = request.user
    # data['vessel'] = Vessels.objects.get(voyage=trip, version=ver).vcode
    data['vessel'] = Vessels.objects.get(voyage=trip).vcode
    data['trip'] = trip
    data['ver'] = ver
    data['container'] = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).order_by('booking')
    return render(request, 'valdata/contlist.html', data)

