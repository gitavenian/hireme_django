# Generated by Django 5.0.6 on 2024-07-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_birthdate_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(max_length=15),
        ),
    ]
