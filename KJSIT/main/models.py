from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    profile_id=models.AutoField(primary_key=True)
    username=models.CharField(null=True, max_length=255)
    
    email=models.EmailField(max_length=60, null=True)    
    def __str__(self):
        return str(self.username) 

# class Job(models.Model):
#     covid=models.FileField()
#     heart=models.FileField()
#     cancer=models.FileField()
#     diabetes=models.FileField()

class Contact_info(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    Query = models.TextField()
    def __str__(self):
        return self.name

'''
class Covid:
    

class Cancer:

class Heart:

class Diabetes:

class Skin:
'''