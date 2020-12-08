from django.contrib import admin
from main.models import HbBlockData, Reception


class HbBlockDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('BlockData', {'fields': ['ownerBlockId', 'url', 'publicKey', 'createDate']}),
        ('BlockDComments', {'fields': ['comments']})
    ]


class ReceptionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Reception', {'fields': ['rid', 'mediatorId', 'receptionistId', 'adopterId', 'status',  'url', 'hash',
                                  'createDate', 'confirmDate']}),
        ('ReceptionComments', {'fields': ['comments', 'opinionDate', 'opinions']})
    ]


admin.site.register(HbBlockData, HbBlockDataAdmin)
admin.site.register(Reception, ReceptionAdmin)
