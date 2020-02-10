def det(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


def zet(request):
    url = "http://localhost:9002/"
    filePath = os.path.join(str(settings.MEDIA_ROOT), "zschedule.pdf")
    wget.download(url, filePath)
    my_data = ''
    response = HttpResponse(my_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filePath)

    return response


def tet(request):
    # apiPDF = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"
    apiPDF = "http://localhost:9002/"

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/pdf'
    }

    # dateVariation = str(datetime.datetime.now())
    # print('filePath >>> {}'.format(dateVariation))
    filePath = os.path.join(str(settings.MEDIA_ROOT), "zschedule.pdf")
    # print('filePath >>> {}'.format(filePath))
    # pdfFile = urllib.URLopener()
    # pdfFile.retrieve(apiPDF, filePath)
    # pdfFile = urllib.request.urlopen(apiPDF, filePath)
    # pdfFile = urllib.request.urlopen(apiPDF)
    req = urllib.request.Request(apiPDF, None, headers)
    # with urllib.request.urlopen(req) as resp:
    #     # creating a pdf reader object
    #     fileReader = PyPDF2.PdfFileReader(resp)

    #     # print the number of pages in pdf file
    #     print(fileReader.numPages)
    #     print('worked!')

    # print('pdfFile.readline >>> {}'.format(pdfFile.readline()))
    # filename = 'DPVesselSchedule.pdf'
    # my_data = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><title>Document</title></head><body><h1>TEST ROD</h1></body></html>'
    my_data = ''
    response = HttpResponse(my_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filePath)

    return response


def bet(HttpResponse):
    apiPDF = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"
    context = {}
    template = "schedule/schedupload.html"
    hasFiles = SchedFILE.objects.filter(date=datetime.date.today())

    print('SCHEDULE GET')
    print(len(hasFiles))
    # for a in hasFiles:
    #     context['data'] = a
    #     print(a)
    if hasFiles == 0:
        # response = urllib.request.urlretrieve(api, file_name)
        # fileheader = request.head(api, allow_redirects=True)
        # header = fileheader.headers
        # content_type = header.get('content-type')
        # if 'pdf' in content_type.lower():

        #     return True
        filename = 'DPVesselSchedule.pdf'
        response = HttpResponse(my_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            filename)

        return response

    # return render(request, template, context)
