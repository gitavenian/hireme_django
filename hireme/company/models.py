from django.db import models

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)  # AutoField is used for auto-incrementing primary keys
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name
    
class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    address = models.CharField(max_length=150 , null=True)
    emails = models.EmailField(
        max_length=100, 
        unique=True,
        null=False,
        default='example@email.com'
    )
    phone_number = models.CharField(
        max_length=20 ,
        null=False,
        default='0000000000'
    )
    city = models.CharField(max_length=50 , default='Aleppo')
    user_name = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=15)
    user_type = models.IntegerField(default=2, null=False)
    image = models.CharField(
        max_length=255 , 
        null=True
    )

    def __str__(self):
        return self.name
