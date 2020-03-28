from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpResponse, Http404

from urllib.request import urlretrieve
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
import csv
import os
import random
import string
import tabula
import re
import io

from .models import SchedFILE, Vessels
# from schedule.views import RamdomColor, getVersion
# Vessels.objects.update_or_create( vslfull="TSMN25", portName="deltaport", vcode="TSMN", vname="", voyage=25, line="ZED", service="ZP9", erdDate="2020-03-11 17:00:00", cutoffDate="2020-03-11 16:00:00", demurrageRFT="2020-03-15", shipETAdate="2020-03-22", shipETAtime="01:00", shipETDdate="2020-03-18 16:00:00" )


@login_required(login_url='login')
def listSchedule(request):
    # > working OK!
    # =============================================
    # this VIEW lists all vessels
    # =============================================    
    data = {}
    monthAhead = datetime.now()+timedelta(days=30)
    monthBehind = datetime.now()-timedelta(days=60)
    data['vessel'] = Vessels.objects.filter(shipETAdate__range=[monthBehind, monthAhead]).order_by('shipETAdate')
    # data['vessel'] = Vessels.objects.filter(shipETAdate__gte=datetime.now()-timedelta(days=21))
    return render(request, 'schedule/schedule.html', data)




def filesSchedule(request):
    # =============================================
    # this VIEW shows a list of files that have been uploaded
    # =============================================
    data = {}
    data['files'] = SchedFILE.objects.all()
    # data['user'] = request.user
    # print(data['user'])
    return render(request, 'schedule/schedfiles.html', data)


# @login_required(login_url='login')
def delSchedule(request, id):
    # =============================================
    # this VIEW deletes the selected item from
    # the database and the corresponding file from storage
    # =============================================

    # Get the PortFile object
    file = SchedFILE.objects.filter(pk=id)

    # Delete the file
    delPDF = os.path.join(str(settings.MEDIA_ROOT), str(file[0].fnamePDF))
    delCSV = os.path.join(str(settings.MEDIA_ROOT), str(file[0].fnameCSV))

    # 2) Deletes the FILES from storage
    if os.path.exists(delPDF):
        # print('DELETED')
        os.remove(delPDF)

    if os.path.exists(delCSV):
        # print('DELETED')
        os.remove(delCSV)        

    # 3) Deletion of DATA from PORTFILE model
    file.delete()

    data = {}
    data['files'] = SchedFILE.objects.all()

    return render(request, 'schedule/schedfiles.html', data)



def randomString(stringLength=4):
    # Generate a random string of fixed length
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))



def downPDF(request):
    
    #  building a unique name for the schedule file being downloaded
    fname = '{}{}{}'.format("sched/schedule_", str(
        datetime.now().strftime("%Y%d%m")), randomString().upper())
    
    # file name definition
    fnameCSV = os.path.join(str(settings.MEDIA_ROOT), '{}{}'.format(fname, '.csv'))
    print('fnameCSV > {}'.format(fnameCSV))
    fnamePDF = os.path.join(str(settings.MEDIA_ROOT), '{}{}'.format(fname, '.pdf'))
    print('fnamePDF > {}'.format(fnamePDF))

    #  URL from where the FILE will be downloaded
    url = "http://localhost:9003/"
    #url = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"

    # save the PDF file
    urlretrieve(url, fnamePDF)

    # 2) convert PDF into CSV file
    tabula.convert_into(fnamePDF, fnameCSV, output_format="csv", pages='all')    

    # 3) Saving file names to Database
    obj, created = SchedFILE.objects.update_or_create(uploaded_by=request.user, fnamePDF=fnamePDF, fnameCSV=fnameCSV)


    return obj.fnameCSV



def saveSchedule(request):

    data = {}
    # CSV file name from the downPDF function
    csv_file = downPDF(request)

    # START reading the file
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    # skip first line
    next(io_string)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    service = ''
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        # get the name of the SERVICE on column[3]
        service = column[3]

        # if the line is not from ZIM then SKIP the line and try the next one
        if "ZP9" in service:
            vslCode = re.findall("[A-Z]*", column[0])[0]
            vslVoyage = re.split("[A-Z]*", column[0])[-1]
            # print(column[0])
            # print('vslCode > {}'.format(vslCode))
            # print('vslVoyage > {}'.format(vslVoyage))
            # test = vslCode + " / " + vslVoyage
            # print('test > {}'.format(test))
            # vesselID = CheckVessel(vslCode + " / " + vslVoyage)            
            # print('vesselID.vcode > {}'.format(vesselID.vcode))

            _, created = Vessels.objects.update_or_create(
                    vnameA = column[0],
                    vnameB = "",
                    description = column[1],
                    portName = "deltaport",
                    line = column[2],
                    service = column[3],
                    erdDate = convertDate(column[4], "full"),
                    cutoffDate = convertDate(column[6], "midway"),
                    demurrageRFT = convertDate(column[7], "min"),
                    shipETAdate = convertDate(column[8], "notime"),
                    shipETAtime = column[9],
                    shipETDdate = convertDate(column[10] + " " + column[11], "midway"),
            )

    # monthAhead = datetime.now()+timedelta(days=30)
    # monthBehind = datetime.now()-timedelta(days=60)
    # data['vessel'] = Vessels.objects.filter(shipETAdate__range=[monthBehind, monthAhead]).order_by('shipETAdate')
    # return render(request, 'schedule/schedule.html', data)
    return redirect('urllistschedule')



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

    # splits the date string into date and time and PM/AM
    check = data.split(' ')
    # print("check[0] > {}".format(check[0]))

    # splits the time string into hour/minute/second
    if len(check) > 1:
        hora = check[1].split(':')
        # print("check[1] > {}".format(check[1]))


    # check which DATE format to use
    if "full" in opt:

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])
        
        newDate = datetime.strptime(data, '%a-%d-%b %H:%M')
        if newDate.year < datetime.today().year:
            data = newDate.replace(year=datetime.today().year)

        # print('FULL data conversion > {}'.format(data))
        # return datetime.strptime(data, '%a-%d-%b %H:%M')
        return data

    elif "midway" in opt:

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        newDate = datetime.strptime(data, '%d-%b %H:%M')
        if newDate.year < datetime.today().year:
            data = newDate.replace(year=datetime.today().year)

        # print('MIDWAY data conversion > {}'.format(data))
        # return datetime.strptime(data, '%d-%b %H:%M')
        return data

    elif "notime" in opt:

        newDate = datetime.strptime(data, '%a-%d-%b')
        if newDate.year < datetime.today().year:
            data = newDate.replace(year=datetime.today().year)

        # print('NOTIME data conversion > {}'.format(data))
        # return datetime.strptime(data, '%a-%d-%b')     
        return data

    elif "min" in opt:

        newDate = datetime.strptime(data, '%d-%b')
        if newDate.year < datetime.today().year:
            data = newDate.replace(year=datetime.today().year)

        # print('MIN data conversion > {}'.format(data))
        # return datetime.strptime(data, '%d-%b')
        return data

    elif "original" in opt:
        # ============================================
        # data sample
        # 11-17-2018 4:41:35 PM
        # 11-19-2018 11:19:22 AM
        # ============================================
        # print("ORIGINAL > {}".format(data))

        # fixes the hour to 24hour format
        if check[-1] == 'PM' and hora[0] != '12':
            hora[0] = int(hora[0]) + 12

        if check[-1] == 'AM' and hora[0] == '12':
            hora[0] = '00'

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1]) + str(':') + str(hora[2])

        newDate = datetime.strptime(data, '%m-%d-%Y %H:%M:%S')
        if newDate.year < datetime.today().year:
            data = newDate.replace(year=datetime.today().year)

        # print('ORIGINAL data conversion > {}'.format(data))
        # return datetime.strptime(data, '%m-%d-%Y %H:%M:%S')
        return data


def CheckVessel(codeVoyage):
    # > working OK!    
    # =============================================
    # this is NOT a VIEW.
    # function called from PORTDT_SaveData to
    # check if the VESSEL data already exists in the database
    # returns either '' or Vessel ID (for Foreign Key)
    # =============================================

    # print("codeVoyage > {}".format(codeVoyage))
    namePieces = codeVoyage.split(' / ')
    vslcode = namePieces[0]+namePieces[1]
    # print("vslcode[0] > {}".format(vslcode[0]))
    # print("vslcode[1] > {}".format(vslcode[1]))
    try:
        # vsl = Vessels.objects.get(Q(vcode=vslcode[0]), Q(voyage=vslcode[1]))
        vsl = Vessels.objects.get(vnameA=vslcode)
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
        return ''


def CreateVessel(code, voy):
    # > NOT working <<<<<<<<<
    # =============================================
    # this is NOT a VIEW.
    # THIS IS NOT WORKING YET
    # this function will create 
    # a VESSEL when it does NOT exist
    # =============================================  
    # Vessels.objects.update_or_create( vslfull="DATE22", portName="deltaport", vcode="DATE", vname="", voyage=22, line="ZED", service="ZP9", erdDate="2020-03-11 17:00:00", cutoffDate="2020-03-11 16:00:00", demurrageRFT="2020-03-15", shipETAdate="2020-03-17", shipETAtime="01:00", shipETDdate="2020-03-18 16:00:00" )  
    vsl = Vessels(vcode=code, voyage=voy)
    vsl.save()
    print("vsl > {}".format(vsl))
    print("vsl.code > {}".format(vsl.vcode))
    return vsl