# Generated by Django 5.0.6 on 2024-07-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(default=1),
        ),
    ]
