# Generated by Django 5.0.6 on 2024-05-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=20)),
                ('photo', models.CharField(max_length=100)),
                ('birthDate', models.DateField()),
                ('language', models.CharField(choices=[('English', 'English'), ('Arabic', 'Arabic'), ('French', 'French')], default='English', max_length=10)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
    ]
