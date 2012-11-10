from django.db import models

# Create your models here.


class Question(models.Model):
		question = models.CharField(max_length=200)
		def __unicode__(self):
				return self.question


class AnswerOption(models.Model):
		question = models.ForeignKey(Question)
		answer = models.CharField(max_length=5000)
		def __unicode__(self):
			return self.question.__unicode__() + self.answer

class ActiveQuestion(models.Model):
		question = models.ForeignKey(Question)
		def __unicode__(self):
			return self.question.__unicode__()
