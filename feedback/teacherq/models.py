from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.

class Question(models.Model):
		question = models.CharField(max_length=200)
		visible = models.BooleanField()
		def __unicode__(self):
				return self.question

class QuestionAnswer(models.Model):
		user = models.ForeignKey(User)
		question = models.ForeignKey(Question)
		answer = models.ManyToManyField(AnswerOption)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # Other fields here
    is_teacher = models.BooleanField()
    is_confused = models.BooleanField()
    def __unicode__(self):
      return self.user.__unicode__()

class UserQuestionAnswer(models.Model):
	user = models.ForeignKey(User)
	answer = models.ForeignKey(AnswerOption)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
