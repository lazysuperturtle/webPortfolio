from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=500)
    finish_date = models.DateTimeField()
    added_date = models.DateField(auto_now=True)
    url = models.CharField(max_length=25)
    completed = models.BooleanField(default=False)
    author_id = models.IntegerField()

    def __str__(self):
        return self.title


class User(models.Model):

    fname = models.CharField(max_length=50)
    sname = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    mail = models.EmailField()
    events = models.ManyToManyField("Event")

    def __str__(self):
        return self.fname.capitalize() + " " + self.sname.capitalize()
