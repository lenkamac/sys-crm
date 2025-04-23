from django.contrib import admin
from .models import Client, ClientFile, Comment


# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone', 'created_at', 'status')
    list_filter = ('created_at', 'status')
    search_fields = ('last_name', 'email')

    ordering = ('-created_at',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Comment)
admin.site.register(ClientFile)
