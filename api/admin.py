from django.contrib import admin
from .models import Initiate, Perform, Termination, Report

admin.site.register(Initiate)
admin.site.register(Perform)
admin.site.register(Termination)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'polis_sery', 'polis_number', 'polis_status', 'insurance_premium', 'insurance_cost')
    list_display_links = ('client_name', 'polis_sery', 'polis_number',)

admin.site.register(Report, ReportAdmin)
