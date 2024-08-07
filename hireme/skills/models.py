from django.db import models

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    jobNature = models.ForeignKey('job.JobNature', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255 , default='skill')
    skill = models.CharField(max_length=255 , default='Front End Developer')
    description = models.TextField(null=True)
    experience = models.FloatField(default=1)
    started_at = models.DateField()

class PreviousJob(models.Model):
    previousJob_id = models.AutoField(primary_key=True)
    jobNature = models.ForeignKey('job.JobNature', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255 , default='some job')
    job = models.CharField(max_length=255 , default='Front End Developer')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    company = models.CharField(max_length=255 , null= False , default= 'Company')
    experience = models.FloatField(default=1.0)
    portfolio = models.CharField(max_length=255 , null=True)
    description = models.TextField()
    recommendation = models.TextField(null=True)
