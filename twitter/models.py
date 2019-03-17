import datetime

from django.contrib.auth.models import User
from django.db import models

TWITTER_MAXIMUM_TWEET_LENGTH = 280
COMMENT_MAXIMUM_LENGTH = 30

class Tweet(models.Model):
    content = models.CharField(max_length=TWITTER_MAXIMUM_TWEET_LENGTH)
    creation_date = models.DateTimeField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.creation_date}] ' \
            f'TWEET by {self.author}: {self.content[:20]}'


class Comment(models.Model):
    content = models.CharField(max_length=COMMENT_MAXIMUM_LENGTH)
    creation_date = models.DateTimeField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return self.content