from django.contrib import admin
from .models import struct, trade, invalid

admin.site.register(struct)
admin.site.register(trade)
admin.site.register(invalid)