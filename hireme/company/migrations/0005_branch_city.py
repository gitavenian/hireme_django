# Generated by Django 5.0.6 on 2024-07-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_branch_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='city',
            field=models.CharField(default='Aleppo', max_length=50),
        ),
    ]
