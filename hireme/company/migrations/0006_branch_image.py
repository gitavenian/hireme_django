# Generated by Django 5.0.7 on 2024-07-25 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_branch_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
