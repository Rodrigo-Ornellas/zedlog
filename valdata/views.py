from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpResponseRedirect

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.contrib.auth import logout

from collections import OrderedDict

import csv
import io
import os
import urllib

from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q

import random

from .models import PortFILE, PortData, Vessels, PortName, Containers, VPDConnector
from .forms import PortFILEForm
# from schedule.views import convertDate

# ====== HOME PAGE ==================================================
# ===================================================================


def index(request):
    # working OK
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
def PORTFL_ListFiles(request):
    # working OK
    # =============================================
    # this VIEW shows a list of files that have been uploaded
    # =============================================
    data = {}
    data['pd'] = PortFILE.objects.all()
    data['user'] = request.user
    # print(data['user'])
    return render(request, 'valdata/portfiles.html', data)


@login_required(login_url='login')
def PORTFL_Del(request, id):
    # working OK
    # =============================================
    # this VIEW deletes the selected item from
    # the database and the corresponding file from storage
    # =============================================

    # Get the PortFile object
    file = PortFILE.objects.filter(pk=id)

    # Delete the file
    delFile = os.path.join(str(settings.MEDIA_ROOT), str(file[0].filename))

    # Get the correcponding PortData
    data = PortData.objects.filter(filefk=id)

    # 1) This deletes the DATA associated with the file from PortData model.
    for row in data:
        row.delete()
        # print(row.serial)

    # 2) Deletes the FILES from storage
    if os.path.exists(delFile):
        # print('DELETED')
        os.remove(delFile)

    # 3) Deletion of DATA from PORTFILE model
    file.delete()

    data = {}
    data['pd'] = PortFILE.objects.all()

    return render(request, 'valdata/portfiles.html', data)


@login_required(login_url='login')
def PORTFL_Upload(request):
    # =============================================
    # this VIEW uploads the csv FILE from the PORT
    # and saves the date to the database
    # =============================================
    prompt = {}
    template = "valdata/csvupload.html"
    
    print("HERE IS WORKING - 00")
    if request.method == 'POST':
        form = PortFILEForm(request.POST, request.FILES)
        print("HERE IS WORKING - 01")
        if form.is_valid():
            print("HERE IS WORKING - 02")
            # print(request.FILES)
            try:
                instance = form.save(commit=False)
                instance.uploaded_by = request.user
                instance.save()

                print("HERE IS WORKING - 03")
                # This gets the file data (PORTData) and saves to database
                stats = PORTDT_SaveData(instance)
                print("stats from PORTFL_Upload > {}".format(stats))
                return redirect('urlvsllist')
            except:
               return redirect('urlmessage', msg='Fatal Error: (from PORTFL_Upload view) error while uploading file.')

    else:
        print("HERE IS WORKING - 04")
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
    # > working OK!
    # =============================================
    # this Function generates 
    # RANDOM color code for STYLING
    # =============================================
 
    for i in range(1,20):
        r = random.randint(0,200)

    for i in range(1,20):        
        g = random.randint(0,200)

    for i in range(1,20):                
        b = random.randint(0,255)

    return str("rgb({},{},{});".format(r,g,b))


def CreateVessel(code, voy):
    # > NOT working <<<<<<<<<
    # =============================================
    # this is NOT a VIEW.
    # THIS IS NOT WORKING YET
    # this function will create 
    # a VESSEL when it does NOT exist
    # =============================================    
    vsl = Vessels(vcode=code, voyage=voy)
    vsl.save()
    print("vsl > {}".format(vsl))
    print("vsl.code > {}".format(vsl.vcode))
    return vsl


def CheckVessel(codeVoyage):
    # > working OK!    
    # =============================================
    # this is NOT a VIEW.
    # function called from PORTDT_SaveData to
    # check if the VESSEL data already exists in the database
    # returns either '' or Vessel ID (for Foreign Key)
    # =============================================

    # print("codeVoyage > {}".format(codeVoyage))
    vslcode = codeVoyage.split(' / ')
    # print("vslcode[0] > {}".format(vslcode[0]))
    # print("vslcode[1] > {}".format(vslcode[1]))
    try:
        # vsl = Vessels.objects.get(Q(vcode=vslcode[0]), Q(voyage=vslcode[1]))
        vsl = Vessels.objects.get(vcode=vslcode[0])
        # print("CHECK VESSEL line 180 > {}".format(vsl))
        
        # This code below would DUPLICATE the VESSEL
        # ==========================================
        # version = vsl.version + 1
        # vsl.pk = None
        # vsl.save()
        # vsl.update(version=version)
        # ==========================================
        return vsl
    except:
        # Vessels.objects.update_or_create( vslfull="DATE22", portName="deltaport", vcode="DATE", vname="", voyage=22, line="ZED", service="ZP9", erdDate="2020-03-11 17:00:00", cutoffDate="2020-03-11 16:00:00", demurrageRFT="2020-03-15", shipETAdate="2020-03-17", shipETAtime="01:00", shipETDdate="2020-03-18 16:00:00" )
        return ''

    

@login_required(login_url='login')
def ListVessels(request):
    # > working OK!
    # =============================================
    # this VIEW lists all the trips
    # function called from PORTDT_SaveData to
    # check if the PORT data already exists in the database
    # returns either '' or Port ID (for Foreign Key)
    # =============================================    

    # try:
    #     vsl = VPDConnector.objects.all().order_by('vessels__checkedDate')
    # except:
    #     vsl = None
    
    vsl = Vessels.objects.all().order_by('-checkedDate')

    data = {}
    data['user'] = request.user
    data['vsl'] = vsl
    return render(request, 'valdata/vsllist.html', data)



@login_required(login_url='login')
def listSchedule(request):
    # > working OK!
    # =============================================
    # this VIEW lists all vessels
    # =============================================    
    data = {}
    data['vessel'] = Vessels.objects.filter(shipETAdate__gte=datetime.now()-timedelta(days=21))
    return render(request, 'valdata/schedule.html', data)



def CheckPort(code):
    # > working OK!
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
    # > working OK!
    # =============================================
    # this VIEW does NOT exist.
    # function called from PORTDT_SaveData to
    # check if the CONTAINER data already exists in the database
    # returns either '' or CONTAINER ID (for Foreign Key)
    # =============================================
    # print("name > {} ***************".format(zname))
    # print("name > {}".format(cname))
    # print("ctype > {}".format(mod))
    # print("dest > {}".format(dest.pk))
    try:
        container = Containers.objects.get(containerID=zname)
    except:
        print('failed! > 1 - CheckContainer')
        try:
            # print("zname > {}".format(zname))
            # print("mod > {}".format(mod))
            # print("dest > {}".format(dest))
            container = Containers(serial=zname, ctype=mod, pod=dest)
            container.save()
        except:
            print('failed! > 2 - CheckContainer <<<<<<')

    return container


@login_required(login_url='login')
def PORTDT_ListData(request):
    # > working OK!
    # =============================================
    # this VIEW uploaded the csv DATA from the PORT
    # and saves the date to the database
    # =============================================
    data = {}
    data['user'] = request.user
    data['csv'] = PortData.objects.all()
    return render(request, 'valdata/csvdata.html', data)


def PORTDT_SaveData(passedFile):
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
    executed = 0
    totrows = 0
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        # counters control
        totrows += 1

        # get the name of the VESSEL
        if vesselID == '':
            vesselID = CheckVessel(column[11])

        # declaring DATE variable
        cDate = '- - -'

        # print ("vesselID > {}".format(vesselID))
        # print ("ALL columns > {} / {} / {} / {} / {} / {} / {}".format(column[0], column[1], column[11],column[3], column[4], column[5], column[6]))
        if vesselID != '':
            
            # counters control
            executed += 1
            print ("ENTERED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< {}".format(executed))

            # Check and Update List of Ports in the DataBase
            portObj, portNAME = CheckPort(column[7])

            # Check and Update List of Containers in the DataBase
            contObject = CheckContainer(column[0], column[1], portObj)
                        
            # convert the TEXT date infor into DATE objects                 # <<<<<<< PROBLEM HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            if column[15] != "":
                try:
                    cDate = convertDate(column[15], "original")
                except:
                    print("ERROR caught")
                    cDate = ""
            else:
                cDate = None

            # Get new version of the UpLoaded Data
            ver = getVersion(column[11].split(" / ")[0])

            # Add VesselPortData connection to the DataBase
            vpd = VPDConnector.objects.update_or_create(vsl=vesselID, version=ver, vcolor=RamdomColor())
        
            print("vesselID.vcode > {}".format(vesselID.vcode))
            _, created = PortData.objects.update_or_create(
                # ** numero de identificacao do container
                filefk      = passedFile,
                vessel      = vesselID,          # vessel object
                connector   = vpd,
                serial      = contObject,
                tipo        = column[1],           # ** tipo e tamanho do container
                location    = column[4],       # trem / truck ou yard
                full        = column[6],           # freight kind = full ou empty
                pod         = portObj,               # ** pod = port of destination
                position    = column[8],       # posição no trem ou truck ou yard
                booking     = column[9],        # ** registro da ZIM
                peso        = column[12],          # peso total do container
                carga       = column[13],         # peso da carga
                arrival     = cDate,            # time of arrival to YARD
                # em reparo ou onhold para proximo navio
                onhold      = column[16],
                commodity   = column[17],     # descrição da carga
                haz         = column[18],           # hazerdous material
                reefer      = column[19],        # quando necessita de refrigeração
                ondock      = column[21],        # arrived to terminal
                oog         = column[22],
                # carga especial com dimensões especiais - necessita de procedimentos especiais
            )


        print ("totrows > {}".format(totrows))
        print ("executed > {}".format(executed))
        # return [totrows, executed]


def getVersion(code):
    # ================================================
    # this is not a VIEW
    # this function checks if the VESSEL exists 
    # and returns the version plus 1
    # ================================================
    try:
        # ver = PortData.objects.get(vcode=code)
        ver = VPDConnector.objects.get(vsl=code)
        print("GET VERSION vessel version > {}".format(ver))
        return ver.version + 1
    except:
        print('getVersion - 0')
        return 0


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
    # data['vessel'] = Vessels.objects.get(voyage=trip, version=ver).vcode
    data['vessel'] = Vessels.objects.get(voyage=trip).vcode
    data['trip'] = trip
    data['ver'] = ver
    data['container'] = PortData.objects.filter(vessel__voyage=trip).filter(version=ver).order_by('booking')
    return render(request, 'valdata/contlist.html', data)


# ====== Vessel DashBoard ==============================================
# ===================================================================


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
    return render(request, 'valdata/contlist.html', data)


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
        

        template = "valdata/vsldash.html"
        return render(request, template, data)
    
    # If there AREN'T any SHIPS
    else:
        return redirect('urlmessage', msg='No data available for this ship.')


# ====== END > Vessel Dashboard ===================================================
# ==========================================================================

def convertDate(data, opt):
    # > working OK!
    # ============================================
    # NOT a VIEW
    # support function
    # > converts date string to date object
    # data sample
    # "Wed-26-Feb 17:00"
    # https://www.programiz.com/python-programming/datetime/strptime
    # ============================================

    if "full" in opt:
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])
        
        print('FULL data conversion > {}'.format(data))
        return datetime.strptime(data, '%a-%d-%b %H:%M')

    elif "midway" in opt:
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        print('MIDWAY data conversion > {}'.format(data))
        return datetime.strptime(data, '%d-%b %H:%M')

    elif "notime" in opt:
        print('NOTIME data conversion > {}'.format(data))
        return datetime.strptime(data, '%a-%d-%b')        
    elif "min" in opt:
        print('MIN data conversion > {}'.format(data))
        return datetime.strptime(data, '%d-%b')
    elif "original" in opt:
        # ============================================
        # data sample
        # 11-17-2018 4:41:35 PM
        # 11-19-2018 11:19:22 AM
        # ============================================
        
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

        print('ORIGINAL data conversion > {}'.format(data))
        return datetime.strptime(data, '%m-%d-%Y %H:%M:%S')