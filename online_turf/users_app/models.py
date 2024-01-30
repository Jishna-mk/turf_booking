from django.db import models
from manager_app.models import TurfList,ManagerProfile
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    turf = models.ForeignKey(TurfList, on_delete=models.CASCADE, null=True)
    game_choices = [
        ('cricket', 'Cricket'),
        ('football', 'Football'),
        ('badminton', 'Badminton'),
        ('fitness', 'Fitness'),
        ('coaching', 'Coaching'),
    ]
    game = models.CharField(max_length=20, choices=game_choices, default='Football')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    date = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
    



class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    manager=models.ForeignKey(ManagerProfile,on_delete=models.CASCADE,null=True,blank=True)
    added_Date = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=200,null=True,blank=True)
    reply = models.BooleanField(default=False)
