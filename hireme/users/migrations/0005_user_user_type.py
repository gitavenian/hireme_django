# Generated by Django 5.0.6 on 2024-07-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_name_user_firstname_user_educationlevel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Normal'), (2, 'Company')], default=1),
        ),
    ]
