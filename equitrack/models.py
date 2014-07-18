import json
import random
import requests
import string
from datetime import datetime
from django.db import models
from equitrack import constants

__author__ = 'kenneth'


class IPartners(models.Model):
    ip_code = models.CharField(max_length=100, blank=True)
    ip_name = models.CharField(max_length=100)
    ip_type = models.CharField(max_length=100, blank=True)
    PCA_number = models.CharField(max_length=100)
    ip_phone = models.CharField(max_length=100)

    def __unicode__(self):
        return self.ip_name


class FACE(models.Model):
    ref = models.CharField(max_length=100)
    partner = models.ForeignKey(IPartners, related_name='face_refs')
    submited_on = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=100, default=0)
    status = models.CharField(blank=True, choices=(('paid', 'paid'), ('cancelled', 'cancelled')), max_length=100)
    date_paid = models.DateTimeField(null=True, blank=True)
    acknowledgment = models.CharField(choices=(('yes', 'yes'), ('no', 'no')), blank=True, max_length=100)

    def __unicode__(self):
        return self.ref

    def generate_number(self):
        N = 8
        self.ref = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    def notify_payment(self):
        response = None
        if self.status == 'paid' and not self.date_paid:
            obj = {
                "flow": constants.FLOW_NUMBER,
                "phone": [self.partner.ip_phone],
                "extra": {
                    "faceref": self.ref,
                    "amount": self.amount
                }
            }
            response = requests.post(constants.START_FLOW_URL, data=json.dumps(obj),
                                     headers={'Content-type': 'application/json',
                                              'Authorization': constants.AUTH_TOKEN})
        return response

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.ref:
            self.generate_number()
        response = self.notify_payment()
        print "response===>", response
        if response:
            try:
                if response.status_code in [200, 201]:
                    self.date_paid = datetime.now()
                else:
                    print response.status_code
                    print response.content
            except Exception as e:
                print e
        super(FACE, self).save()