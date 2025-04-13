from django.contrib import admin
from .models import Lead, LeadFile, Comment


# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'company', 'email', 'phone', 'created_at', 'status', 'priority')

    list_filter = ('created_at', 'status', 'priority')

    search_fields = ('first_name', 'last_name', 'email')

    ordering = ('-created_at',)


# Register your models here.
admin.site.register(Lead, LeadAdmin)

admin.site.register(Comment)
admin.site.register(LeadFile)


