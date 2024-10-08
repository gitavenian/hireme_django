# Generated by Django 5.0.6 on 2024-05-24 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('user_name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=15)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
    ]
