import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from equitrack.models import IPartners, FACE, DCTReport
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
            face = FACE.objects.get(ref__iexact=ref)
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


def dashboard(request):
    f_paid = FACE.objects.filter(status='paid')
    f_reg = FACE.objects.all()
    f_proc = FACE.objects.filter(status=None)
    f_ret = FACE.objects.filter(status='returned')
    d_ack = DCTReport.objects.filter(face__acknowledgment='yes')
    d_imp = DCTReport.objects.filter(status='implemented')
    d_ovr = DCTReport.objects.filter(status='overdue')
    d_proc = DCTReport.objects.filter(status=None)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def add_dct(request):
    values = json.loads(request.POST.get('values', {}))
    DCT = None
    f = None
    for value in values:
        if value.get('label', None) == 'status' and value.get('value').lower() == 'yes':
            DCT = 'implemented'
            continue
        if value.get('label', None) == 'status' and value.get('value').lower() == 'no':
            DCT = 'overdue'
            continue
        if value.get('label', None) == 'face_ref' and value.get('value').lower() == 'valid':
            f = FACE.objects.get(ref__iexact=value.get('text'))
    if DCT and f:
        _DCT = DCTReport.objects.get_or_create(face=f)[0]
        _DCT.status = DCT
        _DCT.save()
        return HttpResponse(status=200)
    return HttpResponse("%s-face, %s-DCT %s"%(str(f), str(DCT), json.dumps(values)))