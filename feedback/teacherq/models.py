from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.


class Question(models.Model):
		question = models.CharField(max_length=200)
		def __unicode__(self):
				return self.question


class AnswerOption(models.Model):
		question = models.ForeignKey(Question)
		answer = models.CharField(max_length=5000)
		count = models.IntegerField()
		def __unicode__(self):
			return self.question.__unicode__() + self.answer

class ActiveQuestion(models.Model):
		question = models.ForeignKey(Question)
		def __unicode__(self):
			return self.question.__unicode__()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # Other fields here
    is_teacher = models.BooleanField()
    is_confused = models.BooleanField()
    def __unicode__(self):
      return self.user.__unicode__()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
