from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end')
    list_filter = ('start',)

    ordering = ('-start',)


admin.site.register(Event, EventAdmin)