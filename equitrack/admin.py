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


def get_amount(obj):
    try:
        return "{:,}".format(int(obj.amount))
    except:
        return obj.amount


def get_status(obj):
    if obj.status:
        return obj.status
    else:
        return "In Process"

def get_acknowledgement(obj):
    if obj.acknowledgment:
        return obj.acknowledgment
    else:
        return ""

get_status.short_description = 'Status'

paid_on.short_description = 'Pain On'

get_acknowledgement.short_description = 'Acknowledgement'

get_amount.short_description = 'Amount'

class IPartnersAdmin(admin.ModelAdmin):
    list_display = ('ip_name', 'PCA_number', 'ip_phone', 'ip_type')


class FACEAdmin(admin.ModelAdmin):
    list_display = ('ref', 'partner', submitedOn, 'amount', get_status, paid_on, get_acknowledgement)

admin.site.register(IPartners, IPartnersAdmin)
admin.site.register(FACE, FACEAdmin)