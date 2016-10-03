from django.contrib import admin
from mailer_server.tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'started_on', 'finished_on', 'started_by', 'name', 'job_id', 'result')
    list_filter = ( 'name', 'result')

    
admin.site.register(Task, TaskAdmin)