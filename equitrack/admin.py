from django.contrib import admin
from equitrack.models import IPartners, FACE

__author__ = 'kenneth'

def submitedOn(obj):
    return obj.submited_on.strftime("%a, %d %b %Y")

submitedOn.short_description = 'Submited On'

def paid_on(obj):
    if obj.date_paid:
        return obj.date_paid.strftime("%a, %d %b %Y")
    else:
        return ""

paid_on.short_description = 'Pain On'


class IPartnersAdmin(admin.ModelAdmin):
    list_display = ('ip_name', 'PCA_number', 'ip_phone', 'ip_type')


class FACEAdmin(admin.ModelAdmin):
    list_display = ('ref', 'partner', submitedOn, 'amount', 'status', paid_on, 'acknowledgment')

admin.site.register(IPartners, IPartnersAdmin)
admin.site.register(FACE, FACEAdmin)