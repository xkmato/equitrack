import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from equitrack.models import IPartners, FACE
import logging

logger = logging.getLogger(__name__)
__author__ = 'kenneth'


@csrf_exempt
def home(request):
    pca_number, amount = None, None
    values = json.loads(request.POST['values'])
    print values
    logger.info(values)
    print type(values)
    logger.info(type(values))
    for value in values:
        print value
        logger.info(value)
        if value.get('label', None) == 'PCA Number' and value.get('value') == 'valid':
            pca_number = value.get('text')
        if value.get('label', None) == 'amount':
            amount = value.get('value')
    response = json.dumps({'error': 'One of the values is missing'})
    if pca_number and amount:
        ip = IPartners.objects.get(PCA_number__iexact=pca_number)
        face = FACE.objects.create(partner=ip)
        face.amount = amount
        face.partner = ip
        face.save()
        response = json.dumps({'faceref': face.ref})
    return HttpResponse(response)


@csrf_exempt
def validate(request):
    print request.POST
    text = request.POST['text']
    print text
    print type(text)
    try:
        IPartners.objects.get(PCA_number__iexact=text)
        response = json.dumps({'valid': 'valid', 'ipnumber':text})
    except IPartners.DoesNotExist as e:
        print e
        response = json.dumps({'valid': 'invalid', 'ipnumber': text})
    return HttpResponse(response)


@csrf_exempt
def acknowledge(request):
    values = json.loads(request.POST.get('values', {}))
    print "POST====>", request.POST
    logger.info(request.POST)
    print values
    logger.info(values)
    ack = None
    face = None
    for value in values:
        print value
        logger.info(value)
        if value.get('label', None) == 'reference' and value.get('value') == 'valid':
            ref = value.get('text')
            face = FACE.objects.get(ref=ref)
            continue
        if value.get('label', None) == 'acknowledgement':
            if value.get('value').lower() == 'yes':
                ack = 'yes'
                continue
            if value.get('value').lower() == 'no':
                ack = 'no'
                continue
    print ack
    logger.info(ack)
    if ack and face:
        face.acknowledgment = ack
        face.save()
    return HttpResponse(status=201)


@csrf_exempt
def validate_face(request):
    text = request.POST.get('text')
    print text
    print type(text)
    try:
        f = FACE.objects.get(ref__iexact=text)
        response = json.dumps({'valid': 'valid', 'ref': f.ref, 'ip_name': f.partner.ip_name})
    except IPartners.DoesNotExist as e:
        print e
        response = json.dumps({'valid': 'invalid', 'ref': text})
    return HttpResponse(response)