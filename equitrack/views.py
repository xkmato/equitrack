import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from equitrack.models import IPartners, FACE

__author__ = 'kenneth'


@csrf_exempt
def home(request):
    pca_number, amount = None, None
    values = json.loads(request.POST.get('values', {}))
    print values
    for value in values:
        print value
        if value.get('label', None) == 'PCA Number' and value.get('value') == 'valid':
            pca_number = value.get('text')
        if value.get('label', None) == 'amount':
            amount = value.get('value')
    response = json.dumps({'error': 'One of the values is missing'})
    if pca_number and amount:
        ip = IPartners.objects.get(PCA_number=pca_number)
        face = FACE.objects.create(partner=ip)
        face.amount = amount
        face.partner = ip
        face.save()
        response = json.dumps({'faceref': face.ref})
    return HttpResponse(response)


@csrf_exempt
def validate(request):
    text = json.loads(request.POST.get('text'))
    try:
        IPartners.objects.get(PCA_number=text)
        response = json.dumps({'valid': 'valid', 'ipnumber':text})
    except IPartners.DoesNotExist as e:
        response = json.dumps({'valid': 'invalid', 'ipnumber':text})
    return HttpResponse(response)


@csrf_exempt
def acknowledge(request):
    values = json.loads(request.POST.get('values', {}))
    print "POST=====>", request.POST
    print values
    ack = None
    s = request.POST.get('steps')
    if type(s) == list:
        face = s[0].split("|")[1].strip()
    else:
        face = s.split("|")[1].strip()
    face = FACE.objects.get(ref=face)
    for value in values:
        print value
        if value.get('label', None) == 'acknowledgement':
            if value.get('value').lower() == 'yes':
                ack = 'yes'
            if value.get('value').lower() == 'no':
                ack = 'no'
    print ack
    if ack:
        face.acknowledgment = ack
        face.save()
    return HttpResponse(status=201)