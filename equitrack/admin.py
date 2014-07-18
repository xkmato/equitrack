from django.contrib import admin
from equitrack.models import IPartners, FACE

__author__ = 'kenneth'


class IPartnersAdmin(admin.ModelAdmin):
    list_display = ('ip_name', 'PCA_number', 'ip_phone', 'ip_type')


class FACEAdmin(admin.ModelAdmin):
    list_display = ('ref', 'partner', 'submitedOn', 'amount', 'status', 'paid_on', 'acknowledgment')

admin.site.register(IPartners, IPartnersAdmin)
admin.site.register(FACE, FACEAdmin)