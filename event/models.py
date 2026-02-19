from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250,blank=True,null=True)
    event_date = models.DateField()
    time = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        default=1
    )
    participant = models.ManyToManyField(User,related_name='revp_event')

    asset = models.ImageField(upload_to='event_asset',  blank=True, null=True,default="event_asset/default.jpg")
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

