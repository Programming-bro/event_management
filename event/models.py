from django.db import models

# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

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
    attended = models.ManyToManyField(Participant)

    def __str__(self):
        self.name

class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

