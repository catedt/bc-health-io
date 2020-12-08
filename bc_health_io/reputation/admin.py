from django.contrib import admin

from reputation.models import Reputation


class ReputationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Reputation', {'fields': ['doctorId', 'email', 'repute', 'createDate', 'updateDate']}),
    ]


admin.site.register(Reputation, ReputationAdmin)
