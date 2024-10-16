from django.contrib import admin
from .models import Community,ElectionOfficer,CommunityAdmin
# Register your models here.

admin.site.register(Community)
admin.site.register(ElectionOfficer)
admin.site.register(CommunityAdmin)