from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from .forms import PortFILEForm
from .models import PortFILE, PortData, Vessels, PortName, Containers
from django.contrib.auth import logout
from django.conf import settings

from collections import OrderedDict
# from .fusioncharts import FusionCharts

from datetime import datetime, timedelta
import csv
import io
import os
import urllib

from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q

import random

# ====== HOME PAGE ==================================================
# ===================================================================


def index(request):
    # =============================================
    # this VIEW triggers the HOMEPAGE
    # if logged it will show MENU of Options
    # if NOT it will just show LOGIN button and a MAIN message
    # =============================================
    data = {}
    data['user'] = request.user
    data['vsl'] = Vessels.objects.all().order_by('-checkedDate')[:3]
    return render(request, 'valdata/index.html', data)


# ====== PORTFILES ==================================================
# ===================================================================

@login_required(login_url='login')
# def portFILES(request):
def PORTFL_ListFiles(request):
    # PORTFL_ListFiles > working OK!
    # =============================================
    # this VIEW shows a list of files that have been uploaded
    # =============================================
    data = {}
    data['pd'] = PortFILE.objects.all()
    data['user'] = request.user
    # print(data['user'])
    return render(request, 'valdata/portfiles.html', data)


# def deleteFile(request, id):
def PORTFL_Del(request, id):
    # PORTFL_Del > working OK!
    # =============================================
    # this VIEW deletes the selected item from
    # the database and the corresponding file from storage
    # =============================================
    file = PortFILE.objects.filter(pk=id)
    delFile = os.path.join(str(settings.MEDIA_ROOT), str(file[0].filename))
    data = PortData.objects.filter(filefk=id)

    # 1) This deletes the DATA associated with the file from PortData model.
    for row in data:
        row.delete()
        # print(row.serial)

    # 2) Deletes the FILES from storage
    if os.path.exists(delFile):
        print('DELETED')
        os.remove(delFile)

    # 3) Deletion of DATA from PORTFILE model
    file.delete()

    data = {}
    data['pd'] = PortFILE.objects.all()

    return render(request, 'valdata/portfiles.html', data)


@login_required(login_url='login')
# def csvupload(request):
def PORTFL_Upload(request):
    # PORTFL_Upload > working OK!
    # =============================================
    # this VIEW uploads the csv FILE from the PORT
    # and saves the date to the database
    # =============================================
    prompt = {}
    template = "valdata/csvupload.html"
    

    if request.method == 'POST':
        form = PortFILEForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            try:
                instance = form.save(commit=False)
                instance.uploaded_by = request.user
                instance.save()
                PORTDT_SaveData(instance)
                # return redirect('urlportfiles')
                return redirect('urlvsllist')
            except:
               return redirect('urlmessage', msg='Fatal Error: error while uploading file.')

    else:
        prompt['form'] = PortFILEForm()
        prompt['user'] = request.user

    return render(request, template, prompt)


# ====== END > PORTFILES ============================================
# ===================================================================

def message(request, msg):
    # > working OK!
    # =============================================
    # this VIEW shows an ERROR MESSAGE on the screen
    # and button to go to the HOME Page
    # =============================================
    data = {}
    data['msg'] = msg
    print(msg)
    template = "valdata/message.html"
    return render(request, template, data)


# ====== PORT CSV DATA ==============================================
# ===================================================================

# def PORTDT_Delete():
    # =============================================
    # this VIEW does NOT exist.
    # PORT DATA is DELETE automatically from DATABASE
    # when corresponding PORT FILE is deleted
    # =============================================

def RamdomColor():    
    for i in range(1,20):
        r = random.randint(0,200)

    for i in range(1,20):        
        g = random.randint(0,200)

    for i in range(1,20):                
        b = random.randint(0,255)

    return str("rgb({},{},{});".format(r,g,b))


def CheckVessel(codeVoyage):
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the VESSEL data already exists in the database
    # returns either '' or Vessel ID (for Foreign Key)
    # =============================================

    # print(" code / voyage > {}".format(codeVoyage))
    code = codeVoyage.split(' / ')[0]
    voy = codeVoyage.split(' / ')[1]
    color = RamdomColor()
    print(color)
    # print(" code > {}".format(code))
    # print(" voyage > {}".format(voyage))

    try:
        # print('started')
        vsl = Vessels.objects.get(vcode=code)
        # print("vsl.checkID > {}".format(vsl.checkID))
        newvsl = Vessels(vcode=code, voyage=voy, checkID=(vsl.checkID + 1), vcolor=vsl.vcolor)
        newvsl.save()
        # print("vsl > {}".format(vsl))
        # print("vsl.code > {}".format(vsl.vcode))
        # print('worked')
    # except Content.DoesNotExist:
    #     print('failed! > 1')
    except:
        print('failed! > 1 - CheckVessel')
        try: 
            # print('started2')
            newvsl = Vessels(vcode=code, voyage=voy, checkID=1,vcolor=color)
            newvsl.save()
            # print("vsl > {}".format(vsl))
            # print("vsl PK > {}".format(vsl.pk))
            # print("vsl.code > {}".format(vsl.vcode))            
            # print('ended2')
        except:
            print('failed! > 2 - CheckVessel')

    return newvsl

@login_required(login_url='login')
def ListVessels(request):
    # =============================================
    # this VIEW lists all the trips
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================    
    data = {}
    data['user'] = request.user
    data['vsl'] = Vessels.objects.all().order_by('-checkedDate')
    return render(request, 'valdata/vsllist.html', data)



def CheckPort(code):
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================

    try:
        port = PortName.objects.get(pcode=code)
    except:
        print('failed! > 1 - CheckPort')
        try:
            port = PortName(pcode=code)
            port.save()
        except:
            print('failed! > 2 - CheckPort')


    return port, port.pcode


def CheckContainer(zname, mod, dest):
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the CONTAINER data already exists in the database
    # returns either '' or CONTAINER ID (for Foreign Key)
    # =============================================
    print("name > {} ***************".format(zname))
    # print("name > {}".format(cname))
    # print("ctype > {}".format(mod))
    # print("dest > {}".format(dest.pk))
    try:
        container = Containers.objects.get(containerID=zname)
    except:
        print('failed! > 1 - CheckContainer')
        try:
            container = Containers(containerID=zname, ctype=mod, leftTo=dest, isActive=True)
            container.save()
        except:
            print('failed! > 2 - CheckContainer <<<<<<')

    return container


@login_required(login_url='login')
def PORTDT_ListData(request):
    # def csvdata(request):
    # PORTDT_ListData
    # =============================================
    # this VIEW uploaded the csv DATA from the PORT
    # and saves the date to the database
    # =============================================
    data = {}
    data['user'] = request.user
    data['csv'] = PortData.objects.all()
    return render(request, 'valdata/csvdata.html', data)


def PORTDT_SaveData(passedFile):
    # def saveCSV(request, passedFile):
    # PORTDT_SaveData
    # ================================================
    # this function reads the CSV file that was UPLOADED
    # and saves the PORT CSV DATA to the database
    # this is not a VIEW that is called from a URL
    # this view is called after the FILE has been UPLOADED
    # ================================================
    print(passedFile.filename)
    csv_file = passedFile.filename
    # print('csvfile > {}'.format(csv_file.name))
    # print('csvfile > {}'.format(os.path.join(
    # settings.MEDIA_ROOT, '/port/',  csv_file['filename'].name)))

    # ERROR treatment
    # let's check if it is a csv file
    # if not csv_file.name.endswith('.csv'):
    #     return messages.error(request, 'THIS IS NOT A CSV FILE')

    # START reading the file
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    vesselID = ''
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        # get the name of the VESSEL
        if vesselID == '':
            vesselID = CheckVessel(column[11])
            # vesselName = column[11]
            # print('1) vessel ID > {}'.format(vesselID.pk))

        # Check and Update List of Ports in the DataBase
        portObj, portNAME = CheckPort(column[7])
        # print('2) port name > {}'.format(portNAME))
        # print('2) port ID > {}'.format(portObj.pk))

        # Check and Update List of Containers in the DataBase
        contObject = CheckContainer(column[0], column[1], portObj)
        # print('3) container > {}'.format(contObject.containerID))

        # CONVERTING the existing DATE format into the
        cDate = '- - -'
        if column[15] != '':
            cDate = convertDate(column[15])
            print(cDate)
        
        _, created = PortData.objects.update_or_create(
            # ** numero de identificacao do container
            filefk=passedFile,
            vessel=vesselID,          # nome do navio
            serial=contObject,
            tipo=column[1],           # ** tipo e tamanho do container
            location=column[4],       # trem / truck ou yard
            full=column[6],           # freight kind = full ou empty
            pod=portObj,               # ** pod = port of destination
            position=column[8],       # posição no trem ou truck ou yard
            booking=column[9],        # ** registro da ZIM
            peso=column[12],          # peso total do container
            carga=column[13],         # peso da carga
            arrival=cDate,            # time of arrival to YARD
            # em reparo ou onhold para proximo navio
            onhold=column[16],
            commodity=column[17],     # descrição da carga
            haz=column[18],           # hazerdous material
            reefer=column[19],        # quando necessita de refrigeração
            ondock=column[21],        # arrived to terminal
            oog=column[22]
            # carga especial com dimensões especiais - necessita de procedimentos especiais
        )


def convertDate(data):
    # PORTDT_formatdate
    # ============================================
    # NOT a VIEW
    # support function for the SAVECsv FUNCTION
    # > converts date string to date object
    # data sample
    # 11-17-2018 4:41:35 PM
    # 11-19-2018 11:19:22 AM
    # ============================================

    print('data conversion > {}'.format(data))
    # splits the date string into date and time and PM/AM
    check = data.split(' ')

    # splits the time string into hour/minute/second
    hora = check[1].split(':')

    # fixes the hour to 24hour format
    if check[-1] == 'PM' and hora[0] != '12':
        hora[0] = int(hora[0]) + 12

    if check[-1] == 'AM' and hora[0] == '12':
        hora[0] = '00'

    # puts the date string back together
    data = str(check[0]) + str(' ') + str(hora[0]) + \
        str(':') + str(hora[1]) + str(':') + str(hora[2])

    return datetime.strptime(data, '%m-%d-%Y %H:%M:%S')

# ====== END > PORTDATA ============================================
# ===================================================================

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
    data['vessel'] = Vessels.objects.get(voyage=trip, checkID=ver).vcode
    data['trip'] = trip
    data['ver'] = ver
    data['container'] = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).order_by('booking')
    return render(request, 'valdata/contlist.html', data)


# ====== Vessel DashBoard ==============================================
# ===================================================================


def DemurrageList(choice, trip, ver):
    # FILTERING THE CONTAINERS IN THE PORT COLLECTING DEMURRAGE
    # SELECT * FROM valdata_portdata WHERE vessel_id=12 AND reefer <> '';
    hoje = datetime.now()
    days7_week = datetime.now()-timedelta(days=7)
    days15_warning = datetime.now()-timedelta(days=15)
    days_critical = datetime.now()-timedelta(days=720)

    if choice == "critical":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).filter(arrival__range=[days_critical, days15_warning])

    if choice == "weekold":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).filter(arrival__range=[days7_week, hoje])

    if choice == "warning":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).filter(arrival__range=[days15_warning, days7_week])

    if choice == "notarrived":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).filter(arrival__contains='- - -')

    if choice == "hazmaterial":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).exclude(haz=u'')

    if choice == "reefer":
        return PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).exclude(reefer=u'')
    


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
    return render(request, 'valdata/contlist.html', data)


@login_required(login_url='login')
def vslSailDate(request, trip, ver, sdate):
    # =============================================
    # this VIEW updates the SAIL date of the vessel
    # 
    # =============================================
    sailDate = Vessels.objects.filter(voyage=trip).filter(checkID=ver).update(saleDate=sdate)


@login_required(login_url='login')
def vsldash(request, trip, ver):
    # =============================================
    # this VIEW shows a DASHBOARD of the 
    # PORTDATA that has been uploaded
    # =============================================
    data = {}

    # Getting the number of Bookings on this Vessel
    bookings = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).aggregate(Count('booking', distinct=True))

    # Getting the number of Containers on this Vessel
    containers = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).aggregate(Count('serial', distinct=True))

    # Adding the total weight of the Containers and Cargo
    tweight = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).aggregate(total_weights=Sum('peso'))

    # Adding the total weight of the Containers and Cargo
    cweight = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).aggregate(total_weights=Sum('carga'))

    # Adding the total weight of the Containers and Cargo
    vdata = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver)

    # Summary of Container Type Data for the PIE Graph
    # GRAPH 1
    ctype = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).values('tipo').annotate(c=Count('tipo')).order_by('-c')
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
    gpod = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).values('pod__pcode').annotate(c=Count('pod')).order_by('-c')
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
    location = PortData.objects.filter(vessel__voyage=trip).filter(vessel__checkID=ver).values('location').annotate(c=Count('location')).order_by('-c')
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
        data['vessel'] = Vessels.objects.get(voyage=trip, checkID=ver).vcode
        data['bookings'] = bookings
        data['containers'] = containers
        data['voyage'] = trip
        data['typeKey'] = typeKey
        data['typeValue'] = typeValue
        data['podKey'] = podKey
        data['podValue'] = podValue
        data['locKey'] = locKey
        data['locValue'] = locValue        
        data['color'] = Vessels.objects.get(voyage=trip, checkID=ver).vcolor
        data['version'] = ver
        data['tweight'] = "{:,}".format(int(tweight['total_weights']/1000)) 
        data['cweight'] = "{:,}".format(int(cweight['total_weights']/1000)) 
        data['weekoldCount'] = DemurrageList("weekold", trip, ver).aggregate(Count('serial', distinct=True))
        data['warningCount'] = DemurrageList("warning", trip, ver).aggregate(Count('serial', distinct=True))
        data['criticalCount'] = DemurrageList("critical", trip, ver).aggregate(Count('serial', distinct=True))
        data['notarrivedCount'] = DemurrageList("notarrived", trip, ver).aggregate(Count('serial', distinct=True))
        data['hazmaterialCount'] = DemurrageList("hazmaterial", trip, ver).aggregate(Count('serial', distinct=True))
        data['reeferCount'] = DemurrageList("reefer", trip, ver).aggregate(Count('serial', distinct=True))
        

        template = "valdata/vsldash.html"
        return render(request, template, data)
    
    # If there AREN'T any SHIPS
    else:
        return redirect('urlmessage', msg='No data available for this ship.')


# ====== END > Vessel Dashboard ===================================================
# ==========================================================================