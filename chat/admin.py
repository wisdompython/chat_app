from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(PrivateRooms)
admin.site.register(DataSource)
admin.site.register(Collection)