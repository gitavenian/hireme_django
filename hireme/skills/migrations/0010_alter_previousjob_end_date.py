# Generated by Django 5.0.7 on 2024-07-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0009_previousjob_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previousjob',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
