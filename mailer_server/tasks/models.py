from django.conf import settings
from django.db import models


class Task(models.Model):
    "A model to save information about an asynchronous task"
    created_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(blank=True, null=True)
    finished_on = models.DateTimeField(blank=True, null=True)
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, related_name='task_created_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    job_id = models.CharField(max_length=128, blank=True, null=True)
    result = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return u'Task: {0}'.format(self.id)