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


class UrlList(models.Model):
    url = models.URLField(max_length=200)


class WordList(models.Model):
    word_id = models.ForeignKey(UrlList, on_delete=models.CASCADE)
    word = models.CharField(max_length=200)


class WordLocation(models.Model):
    url_id = models.ForeignKey(UrlList, on_delete=models.CASCADE)
    word_id = models.ForeignKey(WordList, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)


class Link(models.Model):
    from_id = models.IntegerField()
    to_id = models.IntegerField()


class LinkWords(models.Model):
    word_id = models.ForeignKey(WordList, on_delete=models.CASCADE)
    link_id = models.ForeignKey(Link, on_delete=models.CASCADE)