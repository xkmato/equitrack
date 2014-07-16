import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from equitrack.models import IPartners, FACE

__author__ = 'kenneth'

@csrf_exempt
def home(request):
    text = request.POST.get('text', None)
    print text
    response = json.dumps({'error':'One of the values is missing'})
    if text and len(text) > 1:
        ip = IPartners.objects.get(PCA_number=text[1])
        face = FACE.objects.create(partner=ip)
        face.amount = text[0]
        face.partner = ip
        face.save()
        response = json.dumps({'extras': {'faceref':face.ref}})
    return HttpResponse(response)