from django.contrib import admin
from .models import JobNature, JobAnnouncement, AppliedJob

admin.site.register(JobNature)
admin.site.register(JobAnnouncement)
admin.site.register(AppliedJob)