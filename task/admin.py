from django.contrib import admin
from .models import Task, TaskComment


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'due_time', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('priority', 'title', 'status')

    ordering = ('-created_at',)


class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')

    ordering = ('-created_at',)

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskComment, TaskCommentAdmin)