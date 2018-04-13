from django.db import models
import datetime
from django.utils import timezone


# Create your models here.


class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_data = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class PageInfo(models.Model):
    url = models.URLField(max_length=200)
    text = models.TextField(max_length=20000)
    title = models.TextField(max_length=200)

    def __str__(self):
        return self.title


class Href(models.Model):
    url = models.URLField(max_length=200)
    url_location_id = models.ForeignKey(PageInfo, on_delete=models.CASCADE)
    click_time = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url


class WordList(models.Model):
    url_location_id = models.ForeignKey(PageInfo, on_delete=models.CASCADE)
    word = models.TextField(max_length=200)
    word_location = models.IntegerField()

    def __str__(self):
        return self.word


