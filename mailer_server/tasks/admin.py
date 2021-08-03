from django.contrib import admin
from mailer_server.tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'started_on', 'finished_on', 'started_by', 'name', 'job_id', 'result')
    list_filter = ( 'name', 'result')
    search_fields = ('job_id', 'id', )

    
admin.site.register(Task, TaskAdmin)