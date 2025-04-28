from django.contrib import admin
from .models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('priority', 'title', 'status')

    ordering = ('-created_at',)

admin.site.register(Task, TaskAdmin)