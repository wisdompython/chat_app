from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(DataSource)
admin.site.register(Collection)
admin.site.register(GroupInvite)
admin.site.register(GroupRoomProfile)