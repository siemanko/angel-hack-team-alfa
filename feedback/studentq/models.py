from django.db import models

class Question(models.Model):
    votescore = models.IntegerField()
    text = models.CharField(max_length=200)
    def __unicode__(self):
      return self.text

# Create your models here.
