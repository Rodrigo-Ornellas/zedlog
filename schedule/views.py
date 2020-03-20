from django.shortcuts import render
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpResponse, Http404

from urllib.request import urlretrieve
from django.contrib.auth.models import User
import csv
import os
import random
import string
import tabula
import re
import io

from .models import SchedFILE
from valdata.views import CheckVessel, RamdomColor, getVersion
from valdata.models import Vessels


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
    # url = "http://localhost:9002/"
    # str = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"
    url = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"

    # save the PDF file
    urlretrieve(url, fnamePDF)

    # 2) convert PDF into CSV file
    tabula.convert_into(fnamePDF, fnameCSV, output_format="csv", pages='all')    

    # 3) Saving file names to Database
    dwnld = SchedFILE(uploaded_by=request.user, fnamePDF=fnamePDF, fnameCSV=fnameCSV)
    dwnld.save()

    return dwnld.fnameCSV



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
                    vslfull = column[0],
                    portName = "deltaport",
                    vcode = vslCode,
                    vname = column[1],
                    voyage = vslVoyage,
                    line = column[2],
                    service = column[3],
                    erdDate = convertDate(column[4], "full"),
                    cutoffDate = convertDate(column[6], "mid"),
                    demurrageRFT = convertDate(column[7], "min"),
                    shipETAdate = convertDate(column[8], "notime"),
                    shipETAtime = column[9],
                    shipETDdate = convertDate(column[10] + " " + column[11], "midway"),
                    # checkedDate = autodate,
                    # checkID = getVersion(vesselID.vcode),
                    # vcolor = RamdomColor()
            )

    # data['file'] = Vessels.objects.filter(shipETAdate__gte=datetime.now()-timedelta(days=21))
    data['file'] = Vessels.objects.all()
    return render(request, 'valdata/schedule.html', data)



def convertDate(data, opt):
    # ============================================
    # NOT a VIEW
    # support function
    # > converts date string to date object
    # data sample
    # "Wed-26-Feb 17:00"
    # https://www.programiz.com/python-programming/datetime/strptime
    # ============================================

    print('data conversion > {}'.format(data))

    if opt == "full":
        # ============================================
        # data sample
        # Wed-11-Mar 17:00
        # ============================================
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        return datetime.strptime(data, '%a-%d-%b %H:%M')
    elif opt == "midway":
        # ============================================
        # data sample MIDWAY
        # 11-Mar 16:00
        # ============================================
                
        # splits the date string into date and time and PM/AM
        check = data.split(' ')

        # splits the time string into hour/minute/second
        hora = check[1].split(':')

        # puts the date string back together
        data = str(check[0]) + str(' ') + str(hora[0]) + \
            str(':') + str(hora[1])

        return datetime.strptime(data, '%d-%b %H:%M')
    elif opt == "notime":
        return datetime.strptime(data, '%a-%d-%b')        
    elif opt == "min":
        # ============================================
        # data sample MIN
        # 15-Mar
        # ============================================

        return datetime.strptime(data, '%d-%b')
    elif opt == "original":
        # ============================================
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