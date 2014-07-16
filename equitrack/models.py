import hashlib
from django.db import models

__author__ = 'kenneth'


class IPartners(models.Model):
    ip_code = models.CharField(max_length=100, blank=True)
    ip_name = models.CharField(max_length=100)
    ip_type = models.CharField(max_length=100, blank=True)
    PCA_number = models.CharField(max_length=100)


class FACE(models.Model):
    ref = models.CharField(max_length=100)
    partner = models.ForeignKey(IPartners, related_name='face_refs')
    submited_on = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def generate_number(self):
        m = hashlib.md5()
        m.update(self.pk)
        self.ref = m.digest()

    def save(self, force_insert=False, force_update=False, using=None):
        self.generate_number()
        if self.paid:
            pass
            #Tell API that this fellow has been paid
        super(FACE, self).save()