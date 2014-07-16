from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

__author__ = 'kenneth'

@csrf_exempt
def home(request):
    print request.body
    return HttpResponse(status=201)