from django.http import HttpResponse

__author__ = 'kenneth'


def home(request):
    print request.body
    return HttpResponse(status=201)