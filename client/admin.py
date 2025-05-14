from django.contrib import admin
from .models import Client, ClientFile, Comment


# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone', 'created_at', 'status', 'is_converted')
    list_filter = ('created_at', 'status')
    search_fields = ('last_name', 'email')

    ordering = ('-created_at',)

    def is_converted(self, obj):
        return obj.converted_from_lead is not None
    is_converted.boolean = True
    is_converted.short_description = 'Converted from lead'

admin.site.register(Client, ClientAdmin)
admin.site.register(Comment)
admin.site.register(ClientFile)
