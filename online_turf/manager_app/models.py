from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class ManagerProfile(models.Model):
    Phone_Number=models.IntegerField()
    Address=models.CharField(max_length=250)
    Qualification=models.CharField(max_length=250)
    Designation=models.CharField(max_length=250)
    Profile_Image=models.FileField(upload_to="turf_img",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    


Area_choices=(
    ('Calicut','Calicut'),
    ('Malappuram','Malappuram'),
)


class TurfList(models.Model):
    Turf_ID=models.AutoField(primary_key=True)
    Turf_name=models.CharField(max_length=200)
    Turf_address=models.CharField(max_length=200)
    Turf_price=models.CharField(max_length=200)
    Turf_caption=models.CharField(max_length=200)
    Turf_image=models.ImageField(null=True ,blank=True,upload_to="turf_img")
    Turf_area=models.CharField(max_length=200,choices=Area_choices,default='Calicut')


