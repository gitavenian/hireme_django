# Generated by Django 5.0.7 on 2024-08-04 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_remove_appliedjob_is_accepted_appliedjob_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobannouncement',
            name='preferredToKnow',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
