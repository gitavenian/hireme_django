# Generated by Django 5.1 on 2024-08-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_educationlevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=20),
        ),
    ]
