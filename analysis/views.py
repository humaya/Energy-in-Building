import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from analysis.analysisMethods.dataManipulation import data_manipulation, group_by_day
from analysis.analysisMethods.linearRegression import calculate_lr
from analysis.analysisMethods.svr import svr_calculate
from .forms import UploadFileForm
from django.http import JsonResponse
from .analysisMethods.readCSV import read_csv
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from datetime import date, datetime


def index(request):
    template = loader.get_template('analysis/introduction.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def methodology(request):
    template = loader.get_template('analysis/methodology.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def results(request):
    template = loader.get_template('analysis/results.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@csrf_exempt
@require_POST
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            timeFormat = request.POST.get("timeFormat", "day")
            inputType = request.POST.get("inputType", "temperatures")

            save_path = os.path.join(settings.MEDIA_ROOT[0], file.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            data = read_csv(save_path)
            data = data_manipulation(data)

            if timeFormat == "day":
                data = group_by_day(data)

            data = svr_calculate(data, timeFormat == "day", inputType == "degree_day")
            if inputType == "degree_day":
                data = calculate_lr(data)

            json_string = json.dumps([ob.__dict__ for ob in data], default=json_serial)
            return HttpResponse(json_string, content_type='application/json')
        else:
            print(form.errors)
