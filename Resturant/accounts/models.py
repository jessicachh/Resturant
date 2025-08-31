from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture=models.ImageField(upload_to="profile_picture")
    bio=models.TextField()
    dob=models.DateField(null=True)
    phone=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)



    
    
