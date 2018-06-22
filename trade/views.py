from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Stock
import trade.Trend as pnlalgo
import requests
import json
from django.shortcuts import redirect
import matplotlib.pyplot as plt
def index(request):
    template = loader.get_template('index.html')

    if request.POST:
        url = 'https://api.iextrading.com/1.0/stock/'+request.POST.get('ticker')+'/chart/1y'
        res = requests.get(url)
        results = json.loads(res.content.decode())
        all_prices = []
        for i in results:
            all_prices.append(i['close'])
        [ positions, PnL] = pnlalgo.algo_result(request.POST.get('signal'),request.POST.get('trade'),all_prices)
        # plt.plot(range(0,len(positions)), positions)
        # plt.show()
        # plt.plot(range(0,len(PnL)), PnL)
        # plt.show()
        Stock.objects.create(name=request.POST.get('algo'),pnl=PnL, position=positions )
        # import pdb; pdb.set_trace()
        # return HttpResponseRedirect(reverse('Trade:index'))
        # return HttpResponseRedirect('index')
        return redirect('index')
    else:
        return render(request, 'index.html')
    # return HttpResponse(template.render({'form':form}), request)

def table(request):
    algos = Stock.objects.all()
    template = loader.get_template('table.html')
    return HttpResponse(template.render({'algos':algos}, request))

def chart(request, id):
    # import pdb; pdb.set_trace()
    template = loader.get_template('chart.html')
    return HttpResponse(template.render({}, request))

# def chart(request, id):
#     # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
#     dataSource = {}
#     dataSource['chart'] = {
#         "caption": "Top 10 Most Populous Countries",
#         "showValues": "0",
#         "theme": "zune"
#         }

#     # Convert the data in the `Country` model into a format that can be consumed by FusionCharts.
#     # The data for the chart should be in an array where in each element of the array is a JSON object
#     # having the `label` and `value` as keys.

#     dataSource['data'] = []
#     dataSource['linkeddata'] = []
#     # Iterate through the data in `Country` model and insert in to the `dataSource['data']` list.
#     data =Stock.objects.get(id=request.id)
#     for key in data.pnl :
#       data = {}
#       data['label'] = key.Name
#       data['value'] = key.Population
#       # Create link for each country when a data plot is clicked.
#       data['link'] = 'newchart-json-'+ key.Code
#       dataSource['data'].append(data)

#       # Create the linkData for cities drilldown
#       linkData = {}
#       # Inititate the linkData for cities drilldown
#       linkData['id'] = key.Code
#       linkedchart = {}
#       linkedchart['chart'] = {
#         "caption" : "Top 10 Most Populous Cities - " + key.Name ,
#         "showValues": "0",
#         "theme": "zune"
#         }

#       # Convert the data in the `City` model into a format that can be consumed by FusionCharts.
#       linkedchart['data'] = []
#       # Filtering the data base on the Country Code
#       for key in City.objects.all().filter(CountryCode=key.Code):
#           arrDara = {}
#         arrDara['label'] = key.Name
#         arrDara['value'] = key.Population
#         linkedchart['data'].append(arrDara)

#       linkData['linkedchart'] = linkedchart
#       dataSource['linkeddata'].append(linkData)

#     # Create an object for the Column 2D chart using the FusionCharts class constructor
#     column2D = FusionCharts("column2D", "ex1" , "600", "350", "chart-1", "json", dataSource)
#     return render(request, 'index.html', {'output': column2D.render()})
