# Generated by Django 5.0.7 on 2024-07-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=10),
        ),
    ]
