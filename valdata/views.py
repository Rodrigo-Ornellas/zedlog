from django.shortcuts import render, redirect
from datetime import datetime
from django.conf import settings

# from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import permission_required, login_required
# from django.contrib import messages
from django.contrib.auth import logout

# from collections import OrderedDict

import csv
import io
import os
# import urllib

import random

from .models import PortFILE, PortData, VPDConnector
from .forms import PortFILEForm

from schedule.models import Vessels
from schedule.views import CheckVessel

from inventory.models import Containers
from inventory.views import CheckContainer

from portname.models import PortRegistry
from portname.views import CheckPort

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
    

    if request.method == 'POST':
        form = PortFILEForm(request.POST, request.FILES)

        if form.is_valid():

            # print(request.FILES)
            # try:
                instance = form.save(commit=False)
                instance.uploaded_by = request.user
                instance.save()

                # This gets the file data (PORTData) and saves to database
                try:
                    PORTDT_SaveData(instance)
                    return redirect('urlcsvdata')
                except:
                    return redirect('urlmessage', msg='Fatal Error: (from PORTDT_SaveData view) error while uploading file.')
            # except:
            #    return redirect('urlmessage', msg='Fatal Error: (from PORTFL_Upload view) error while uploading file.')

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




# @login_required(login_url='login')
# def ListVessels(request):
#     # > working OK!
#     # =============================================
#     # this VIEW lists all the trips
#     # function called from PORTDT_SaveData to
#     # check if the PORT data already exists in the database
#     # returns either '' or Port ID (for Foreign Key)
#     # =============================================    

#     # try:
#     #     vsl = VPDConnector.objects.all().order_by('vessels__checkedDate')
#     # except:
#     #     vsl = None
    
#     vsl = Vessels.objects.all().order_by('-checkedDate')

#     data = {}
#     data['user'] = request.user
#     data['vsl'] = vsl
#     return render(request, 'valdata/vsllist.html', data)




# def CheckPort(code):
#     # > working OK!
#     # =============================================
#     # this VIEW does NOT exist.
#     # function called from PORTDT_SaveData to
#     # check if the PORT data already exists in the database
#     # returns either '' or Port ID (for Foreign Key)
#     # =============================================
#     try:
#         port = PortRegistry.objects.get(pcode=code)
#     except:
#         print('failed! > 1 - CheckPort')
#         try:
#             port = PortRegistry(pcode=code)
#             port.save()
#         except:
#             print('failed! > 2 - CheckPort')

#     return port, port.pcode





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

    # loop through each column in each line    
    vesselID = ''
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        # PRINT ALL COLUMNS
        print(column)
        print('{} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {} @ {}'.format(column[0], column[1], column[2],column[3],column[4],column[5],column[6],column[7],column[8],column[9],column[10],column[11],column[12],column[13],column[14],column[15],column[16],column[17],column[18],column[19],column[20],column[21],column[22],column[23]))

        # get the name of the VESSEL
        if vesselID == '':
            vesselID = CheckVessel(column[11])

        # declaring DATE variable
        cDate = '- - -'

        # print ("vesselID > {}".format(vesselID))
        if vesselID != '':
            
            # Check and Update List of Ports in the DataBase
            portObj = CheckPort(column[7])

            # Check and Update List of Containers in the DataBase
            contObject = CheckContainer(column[0], column[1], portObj)
                        
            # convert the TEXT date infor into DATE objects 
            if column[15] != "":
                try:
                    # print("cDATE > {}".format(column[15]))
                    cDate = simpleConvertDate(column[15])
                except:
                    print("ERROR caught -> LINE 307 -> DATE")
                    cDate = ""
            else:
                cDate = None

            # Get new version of the UpLoaded Data
            ver = getVersion(vesselID)

            # print("version > {}".format(ver))
            # print("color > {}".format(RamdomColor()))
            # Add VesselPortData connection to the DataBase
            vpd, created = VPDConnector.objects.update_or_create(vsl=vesselID, version=ver, vcolor=RamdomColor())
            
            # print("VPDConnerctor > {}".format(vpd))
            # print("vesselID.vcode > {}".format(vesselID.vnameA))
            # print(" linha {}".format(executed))
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
                oog         = column[22]
                # carga especial com dimensões especiais - necessita de procedimentos especiais
            )

            # return 'OKK > PortData saved SUCCESSFULLY!'
        # else:
            # return 'ERR > PortData ERROR - data NOT saved!'

        # print('<<<<<<<      next ITEM      >>>>>>')


def getVersion(code):
    # ================================================
    # this is not a VIEW
    # this function checks if the VESSEL exists 
    # and returns the version plus 1
    # ================================================
    try:
        ver = VPDConnector.objects.get(vsl=code)
        print("GET VERSION vessel version > {}".format(ver.version + 1))
        return ver.version + 1
    except:
        print('getVersion => 0')
        return 0


# ====== END > PORTDATA ============================================
# ===================================================================


def simpleConvertDate(data):
    # > working OK!
    # ============================================
    # NOT a VIEW
    # support function
    # > converts date string to date object
    # https://www.programiz.com/python-programming/datetime/strptime
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

    # print('ORIGINAL data conversion > {}'.format(data))
    return datetime.strptime(data, '%m-%d-%Y %H:%M:%S')