import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from equitrack.models import IPartners, FACE

__author__ = 'kenneth'


@csrf_exempt
def home(request):
    pca_number, amount = None, None
    values = request.POST.get('values', {})
    print values
    for value in values:
        print value
        if value.get('label', None) == 'PCA Number':
            pca_number = value.get('value')
        if value.get('label', None) == 'PCA Number':
            amount = value.get('value')
    response = json.dumps({'error': 'One of the values is missing'})
    if pca_number and amount:
        ip = IPartners.objects.get(PCA_number=pca_number)
        face = FACE.objects.create(partner=ip)
        face.amount = amount
        face.partner = ip
        face.save()
        response = json.dumps({'extras': {'faceref': face.ref}})
    return HttpResponse(response)