def makeJSON(field, vesselName):
    # GRAPH_makejson
    # =============================================
    # SUPPORT function for the DASHBOARD graphs functionality
    # =============================================
    query = field
    data = list(PortData.objects.values_list(query, flat=True).filter(
        vessel=vesselName))

    # print(data)
    # python dictionary that will contain the JSON object
    # with the quantity of variations existing in the selected field
    result = []

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for item in data:
        # check if exists in unique_list or not
        if item not in unique_list:
            unique_list.append(item)

    # print(unique_list)
    # print(data)
    for item in unique_list:
        myJSON = {}
        myJSON['label'] = item
        myJSON['value'] = data.count(item)
        result.append(myJSON)

    return result


def barTYPES(width, height, vessel):
    # =====================================
    #       BAR GRAPH
    # =====================================
    # Preparing the chart data

    # The `chartConfig` dict contains key-value pairs of data for chart ATTRIBUTES
    barConfig = OrderedDict()
    barConfig["caption"] = "Container TYPES"
    barConfig["yAxisName"] = "Qty of Containers"
    barConfig["theme"] = "fusion"

    # Chart DATA is passed to the `barData` parameter, like a dictionary in the form of key-value pairs.
    barData = OrderedDict()

    # saves the configuration in the barData
    barData["chart"] = barConfig
    barData["data"] = []

    # saves the DATA in the barData using the makeJSON function
    barData['data'] = makeJSON('tipo', vessel)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    return FusionCharts("column2d", "myFirstChart",
                        width, height, "bar-container", "json", barData)



def graph(request):
    width = 384
    height = 200
    vssl = "TSMN / 21"
    # =====================================
    #       BAR GRAPH
    # =====================================
    # Preparing the chart data

    # The `chartConfig` dict contains key-value pairs of data for chart ATTRIBUTES
    barConfig = OrderedDict()
    barConfig["caption"] = "Container TYPES"
    barConfig["yAxisName"] = "Qty of Containers"
    barConfig["theme"] = "fusion"

    # Chart DATA is passed to the `barData` parameter, like a dictionary in the form of key-value pairs.
    barData = OrderedDict()

    # saves the configuration in the barData
    barData["chart"] = barConfig
    barData["data"] = []

    # saves the DATA in the barData using the makeJSON function
    barData['data'] = makeJSON('tipo', vssl)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("column2d", "myFirstChart",
                            width, height, "bar-container", "json", barData)

    # =====================================
    #       PIE GRAPH
    # =====================================
    # Preparing the chart data
    # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    # pieData = OrderedDict()
    # dataSource = makeJSON('location')
    # print(dataSource)
    # pieData["data"] = dataSource
    # print(type(pieData["data"]))

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    # chartConfig = OrderedDict()
    # pieConfig = {
    #     "chart": {
    #         "animation": True,
    #         "animationDuration": "1",
    #         "palette": "5",
    #         "caption": "Stats for Vessel Destinations",
    #         "subCaption": "Locations",
    #         "captionOnTop": True,
    #         "bgColor":  "#ffb6c1",
    #         "slicingDistance": "30",
    #         "enableRotation": True,
    #         "pieYScale": "80",
    #         "enableSmartLabels": "0",
    #         "startingAngle": 200,
    #         "showPercentValues": "1",
    #         "decimals": "1",
    #         "useDataPlotColorForLabels": "1",
    #         "theme": "fusion"
    #     }
    # }

    # pieConfig = {
    #     "chart": {"caption": "Stats for Vessel Destinations", "theme": "umber"}
    # }

    # pieData["chart"] = pieConfig

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `pieData` parameter.
    # print('pieData > {}'.format(pieData))
    zimPie = FusionCharts("pie2d", "locationpie3d", width, height, "pie-container", "json", """{
                              "chart": {"caption": "Contanier LOCATION", "theme": "Fusion"},
                            'data': [{'label': 'RAILCAR', 'value': 229}, {'label': 'YARD', 'value': 20}, {'label': 'TRAIN', 'value': 19}]
                          }""")

    # =====================================
    #       MAP GRAPH
    # =====================================
    # Preparing the chart data
    # Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
    # pieData = OrderedDict()
    # dataSource = makeJSON('location')
    # print(dataSource)
    # pieData["data"] = dataSource
    # print(type(pieData["data"]))

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    # chartConfig = OrderedDict()
    # pieConfig = {
    #     "chart": {
    #         "animation": True,
    #         "animationDuration": "1",
    #         "palette": "5",
    #         "caption": "Stats for Vessel Destinations",
    #         "subCaption": "Locations",
    #         "captionOnTop": True,
    #         "bgColor":  "#ffb6c1",
    #         "slicingDistance": "30",
    #         "enableRotation": True,
    #         "pieYScale": "80",
    #         "enableSmartLabels": "0",
    #         "startingAngle": 200,
    #         "showPercentValues": "1",
    #         "decimals": "1",
    #         "useDataPlotColorForLabels": "1",
    #         "theme": "fusion"
    #     }
    # }

    # pieConfig = {
    #     "chart": {"caption": "Stats for Vessel Destinations", "theme": "umber"}
    # }

    # pieData["chart"] = pieConfig

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `pieData` parameter.
    # print('pieData > {}'.format(pieData))
    pod = FusionCharts("maps/world", "worldmap", 800, 600, "map-container", "json",
                       """{
                                "chart": {
                                    "showlegend": 0,
                                    "caption": "Port of DESTINATION",
                                    "nullentityfillcolor": "#D8BFD8",
                                    "showmarkerlabels": "0",
                                    "showentitytooltip": "0",
                                    "showentityhovereffect": "0",
                                    "theme": "fusion"
                                },
                                "markers": {
                                    "items": [
                                                {
                                                    "id": "lon",
                                                    "shapeid": "we-anchor",
                                                    "x": "190.23",
                                                    "y": "350.9",
                                                    "label": "Chile",
                                                    "value": "1",
                                                    "tooltext": "In Chile, WeWork has <b>$value</b> co-working location"
                                                },
                                                {
                                                    "id": "Brazil",
                                                    "shapeid": "we-anchor",
                                                    "x": "250.14",
                                                    "y": "260.9",
                                                    "label": "Brazil",
                                                    "value": "3",
                                                    "tooltext": "In Brazil, WeWork has <b>$value</b> co-working locations"
                                                }
                                    ],
                                    "shapes": [
                                                {
                                                    "id": "we-anchor",
                                                    "type": "image",
                                                    "url": "https://cdn3.iconfinder.com/data/icons/iconic-1/32/map_pin_fill-512.png",
                                                    "xscale": "4",
                                                    "yscale": "4"
                                                }
                                    ]
                                }
                    }""")

    # =====================================
    #       PIE2 GRAPH >
    # =====================================

    onhold = makeJSON('oog', vssl)
    print(onhold)
    arrivedPie = FusionCharts("arrivedPie", "arrivedPie2d", width, height, "pie2-container", "json", """{
                              "chart": {"caption": "Contanier ONDOCK", "theme": "Fusion"},
                            'data': [{'label': 'N', 'value': 242}, {'label': '', 'value': 7}, {'label': 'Y', 'value': 19}]
                          }""")

    return render(request, 'valdata/graph.html', {
        'pie': zimPie.render(),
        'column2D': column2D.render(),
        'map': pod.render(),
        'pie2': arrivedPie.render(),
    })


# def logout_view(request):
#     template = "registration/logged_out.html"
#     logout(request)
#     return render(request, template)


# def upload(request):
#     data = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         data['url'] = fs.url(name)
#         data['user'] = request.user
#         # print(uploaded_file.size)
#     return render(request, 'valdata/upload.html', data)


# @permission_required('admin.can_add_log_entry')
# def upload_portdata(request):
#     data = {}
#     if request.method == 'POST':
#         form = PortDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/portdata/')
#     else:

#         data['form'] = PortDataForm()
#         data['user'] = request.user
#     return render(request, 'valdata/upload_portdata.html', data)

# @permission_required('admin.can_add_log_entry')
# def csvuploadORG(request):
#     context = {}
#     print(request.FILES)
#     if request.method == 'POST':
#         form = PortDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         context['form'] = PortDataForm()
#         context['user'] = request.user

#     # declaring template
#     template = "valdata/csvupload.html"
#     data = PortData.objects.all()
#     # prompt is a context variable that can have different values      depending on their context
#     prompt = {
#         'order': 'Please follow the order pre-defined!',
#         'profiles': data
#     }
#     # GET request returns the value of the data with the specified key.
#     if request.method == "GET":
#         print(request)
#         return render(request, template, prompt)

#     csv_file = request.FILES['file']
#     # let's check if it is a csv file
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, 'THIS IS NOT A CSV FILE')

#     data_set = csv_file.read().decode('UTF-8')
#     io_string = io.StringIO(data_set)
#     next(io_string)

#     template = "valdata/csvloaded.html"
#     context = {}
#     context['count'] = 0
#     vesselName = ''
#     teste = 0

#     # setup a stream which is when we loop through each line we are able to handle a data in a stream
#     for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#         if vesselName == '':
#             vesselName = column[11]
#             teste += 1
#             print('%s - Vessel Name: %s' % (str(teste), vesselName))

#         # column[15] = datetime.strftime(column[15], '%m-%d-%Y %H:%M:%S')
#         # column[15] = convertDate(column[15])
#         if column[15] != '':
#             column[15] = convertDate(column[15])

#         # print(column[15])
#         context['count'] += 1
#         _, created = PortData.objects.update_or_create(
#             serial=column[0],         # ** numero de identificacao do container
#             tipo=column[1],           # ** tipo e tamanho do container
#             location=column[4],       # trem / truck ou yard
#             full=column[6],           # freight kind = full ou empty
#             pod=column[7],            # ** pod = port of destination
#             position=column[8],       # posição no trem ou truck ou yard
#             booking=column[9],        # ** registro da ZIM
#             vessel=column[11],        # nome do navio
#             peso=column[12],          # peso total do container
#             carga=column[13],         # peso da carga
#             arrival=column[15],       # time of arrival to YARD
#             onhold=column[16],        # em reparo ou onhold para proximo navio
#             commodity=column[17],     # descrição da carga
#             haz=column[18],           # hazerdous material
#             reefer=column[19],        # quando necessita de refrigeração
#             ondock=column[21],        # arrived to terminal
#             oog=column[22]
#             # carga especial com dimensões especiais - necessita de procedimentos especiais
#         )

#     # print('Vessel Name: %s' % (vesselName))
#     # context['data'] = PortData.objects.filter(vessel=vesselName)
#     context['data'] = PortData.objects.all()
#     # print(context['data'])
#     return render(request, template, context)


# def dload_schedule(request):
#     template = "valdata/schedule_loaded.html"
#     context = {}
#     url = "http://webservices.globalterminalscanada.com/sites/default/files/DPVesselSchedule.pdf"
#     schedfile = urllib.URLopener()
#     schedfile.retrieve(url, "DPVesselSchedule.pdf")

#     if request.method == 'POST':
#         form = PortFILEForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(request.FILES)
#             saveCSV(request, request.FILES)
#             form.save()
#             return redirect('urlportfiles')

#     else:
#         prompt['form'] = PortFILEForm()
#         prompt['user'] = request.user

#     return render(request, template, prompt)