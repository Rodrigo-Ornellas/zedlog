from .models import SchedFILE
import datetime
from datetime import date
from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.request import urlretrieve
import os
# import PyPDF2
import random
import string


def randomString(stringLength=4):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))


def readPDF(fname):
    # =================================================
    # Function to read downloaded Port PDF Schedule FILE
    # =================================================

    # creating a pdf file object
    pdfFileObj = open(fname, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    print('Number of Pages > {}'.format(pdfReader.numPages))

    # creating a page object
    pageObj = pdfReader.getPage(0)

    # extracting text from page
    print('text from PDF page >> {}'.format(pageObj.extractText()))

    # closing the pdf file object
    pdfFileObj.close()


def downloadSched(request):
    # =================================================
    # Function to DOWNLOAD the Port PDF Schedule from their site
    # =================================================

    #  URL from where the FILE will be downloaded
    url = "http://localhost:9002/"
    # url = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"

    #  building a unique name for the schedule file being downloaded
    prefix = "sched/schedule_"
    fileName = '{}{}{}{}'.format(prefix, str(
        date.today().strftime("%Y%d%m")), randomString().upper(), '.pdf')
    # print('FILENAME >> {}'.format(fileName))
    dst = os.path.join(str(settings.MEDIA_ROOT), fileName)
    # print('XET >> {}'.format(dst))

    # downloading the file
    urlretrieve(url, dst)

    # saving the new downloaded file information to the database
    dwnld = SchedFILE(uploaded_by=request.user, filename=dst)
    dwnld.save()

    readPDF(dst)
    print('\n============ PDF read  ============\n')

    # building the response of the view and returning
    my_data = ''
    response = HttpResponse(my_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(dst)

    return response
