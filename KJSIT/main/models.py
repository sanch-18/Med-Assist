from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    profile_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=255, null=True)
    email=models.EmailField(max_length=60, null=True)    
    def __str__(self):
        return str(self.username) 

class History(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    app = models.CharField(max_length=8)
    disease = models.CharField(max_length=20, null=True)
    result = models.CharField(max_length=10)
    probability = models.FloatField(null=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.timestamp) 

    def save(self, *args, **kwargs):
        super(History, self).save(*args, **kwargs)  

class Contact_info(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    Query = models.TextField()
    def __str__(self):
        return self.name
