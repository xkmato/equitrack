import hashlib
from random import random
from django.db import models

__author__ = 'kenneth'


class IPartners(models.Model):
    ip_code = models.CharField(max_length=100, blank=True)
    ip_name = models.CharField(max_length=100)
    ip_type = models.CharField(max_length=100, blank=True)
    PCA_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.ip_name


class FACE(models.Model):
    ref = models.CharField(max_length=100)
    partner = models.ForeignKey(IPartners, related_name='face_refs')
    submited_on = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=100, default=0)
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def __unicode__(self):
        return self.partner.ip_name + "FACEs"

    def generate_number(self):
        m = hashlib.md5()
        m.update(str(random()))
        self.ref = m.digest()

    def save(self, force_insert=False, force_update=False, using=None):
        self.generate_number()
        if self.paid:
            pass
            #Tell API that this fellow has been paid
        super(FACE, self).save()