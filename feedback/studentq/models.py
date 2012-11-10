from django.db import models

class Question(models.Model):
    votescore = models.IntegerField()
    text = models.CharField(max_length=200)

# Create your models here.
