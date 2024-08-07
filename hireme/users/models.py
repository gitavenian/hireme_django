from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime 

class User(models.Model):
    NORMAL = 1
    COMPANY = 2

    USER_TYPE_CHOICES = [
        (NORMAL, 'Normal'),
        (COMPANY, 'Company'),
    ]

    user_id = models.AutoField(
        primary_key=True
    )
    firstName = models.CharField(
        max_length=75,
        null=False,     
    )
    lastName = models.CharField(
        max_length=75,
        default='ian'
    )
    email = models.EmailField(
        max_length=100, 
        unique=True,
        null=False
    )
    address = models.CharField(
        max_length=150
    )
    phone_number = models.CharField(
        max_length=20 , 
        null=False
    )
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', _('Male')),
            ('Female', _('Female')),
        ],
        default='choose',
        null= False
    )
    photo = models.CharField(
        max_length=255 , 
        null=True
    )
    phone_number = models.CharField(
        max_length=15 ,
        null=False,
        default='0000000000'
    )
    city = models.CharField(
        max_length=15,
        null= False,
        default='Aleppo'
    )
    educationLevel = models.CharField(
        max_length=20,
        null= False,
        default='Bachelor'
    )
    birthDate = models.DateField(null=True)
    language = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=15 , null=False)
    facebook_link = models.CharField(max_length=45, null=False, default='default_facebook_link')
    behance_link = models.CharField(max_length=45 , null=True)
    instagram_link = models.CharField(max_length=45 , null=True)
    github_link = models.CharField(max_length=45 ,null=True)
    user_type = models.IntegerField(default=NORMAL, null=False)

    def save(self, *args, **kwargs):
        # Format the birthDate to dd-mm-yyyy before saving
        if isinstance(self.birthDate, str):
            self.birthDate = datetime.strptime(self.birthDate, '%d-%m-%Y').date()
        super(User, self).save(*args, **kwargs)

    def get_birthdate_formatted(self):
        return self.birthDate.strftime('%d-%m-%Y')
