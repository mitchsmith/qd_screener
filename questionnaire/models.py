from django.db import models
import datetime

class Study(models.Model):
    created_on      = models.DateTimeField(auto_now=True)
    protocol_number = models.SlugField()

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "studies"

class Questionnaire(models.Model):
    created_on          = models.DateTimeField(auto_now=True)
    study               = models.ForeignKey(Study, related_name='parent_study')
    description         = models.TextField(null=True, blank=True)
    sub_title           = models.CharField(max_length=512, null=True, blank=True, default='')
    title               = models.CharField(max_length=32, default='')
    overline_text       = models.CharField(max_length=128, null=True, blank=True)

class QuestionnaireManager(models.Model):
        current_questionnaire    = models.ForeignKey(Questionnaire)

class Question(models.Model):
    created_on           = models.DateTimeField(auto_now=True)
    question             = models.CharField(max_length=256)
    questionnaire         = models.ForeignKey(Questionnaire, related_name='parent_questionnaire')
    sequence_order       = models.IntegerField(blank=False, null=False)
    related_content_link = models.CharField(max_length=512, blank=True, default='') 
    related_content_text = models.CharField(max_length=512, blank=True, default='')

class Answer(models.Model):
    created_on           = models.DateTimeField(auto_now=True)
    answer               = models.CharField(max_length=256)
    question             = models.ForeignKey(Question)
    is_eligible          = models.BooleanField(default=False, help_text='')
    sequence_order       = models.IntegerField(blank=False, null=False)
