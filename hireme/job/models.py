from django.db import models
from users.models import User
class JobNature(models.Model):
    jobNature_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class JobAnnouncement(models.Model):
    jobAnnouncement_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=50)
    job_description = models.TextField()
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)
    jobNature = models.ForeignKey(JobNature, on_delete=models.CASCADE)  # Job nature is different from skills
    main_skill = models.CharField(max_length=50)  # Main skill as a string
    soft_skill = models.CharField(max_length=50, null=True, blank=True)  # Soft skill as a string
    preferredToKnow = models.CharField(max_length=50, null=True, blank=True)  # Soft skill as a string
    isAvailable = models.BooleanField(default=True)
    createdAt = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Any', 'Any')], default='Any')
    educationLevel = models.CharField(max_length=50, null=False, default='Bachelor')
    salary = models.FloatField()
    type_of_employment = models.CharField(max_length=50, default='Full-time', null=False)
    experience = models.IntegerField(null=False, default=0)

class AppliedJob(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('To be Interviewed', 'To be Interviewed'),
    ]
    
    appliedJob_id = models.AutoField(primary_key=True)
    jobAnnouncement = models.ForeignKey(JobAnnouncement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=17, choices=STATUS_CHOICES, default='Waiting')
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.firstName}'s application for {self.jobAnnouncement.job_title}"

class Interview(models.Model):
    interview_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_announcement = models.ForeignKey(JobAnnouncement, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=255)

    def __str__(self):
        return f"Interview for {self.user.firstName} - {self.job_announcement.job_title}"