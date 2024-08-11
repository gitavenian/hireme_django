from django.core.management.base import BaseCommand
from django.utils import timezone
from job.models import JobAnnouncement, User, AppliedJob

class Command(BaseCommand):
    help = 'Automatically applies users from ID 15 to 55 to a specified job'

    def add_arguments(self, parser):
        parser.add_argument('job_announcement_id', type=int, help='ID of the JobAnnouncement to apply to')

    def handle(self, *args, **options):
        job_announcement_id = options['job_announcement_id']
        try:
            job_announcement = JobAnnouncement.objects.get(pk=job_announcement_id)
            for user_id in range(15, 56):  # From user 15 to 55
                user = User.objects.get(pk=user_id)
                # Check if application already exists
                if not AppliedJob.objects.filter(jobAnnouncement=job_announcement, user=user).exists():
                    AppliedJob.objects.create(
                        jobAnnouncement=job_announcement,
                        user=user,
                        status='Applied',
                        current_date=timezone.now()
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully applied user {user_id} to job {job_announcement_id}'))
                else:
                    self.stdout.write(self.style.WARNING(f'User {user_id} has already applied to job {job_announcement_id}'))
        except JobAnnouncement.DoesNotExist:
            self.stdout.write(self.style.ERROR('Job announcement not found.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User ID {user_id} not found.'))
