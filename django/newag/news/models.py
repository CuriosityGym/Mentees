# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Importing to sublclass(inheriting) models
# Create your models here.
class Feed(models.Model):
    feed_choices=(('SPORTS','Sports'),
                ('CURRENT AFFAIRS','Current Affairs'),
                ('TECHNOLOGY' , 'Technology'),
                ('POLITICS' , 'Politics'),
                ('LIFESTYLE' , 'LifeStyle'),
                ('HEALTH', 'Health'),
                ('ADVERTISEMENTS','Advertisements'),
                ('ECONOMY','Economy'),
                ('TRAVEL','Travel'),
                ('WORLD NEWS','World News'),
                ('LOCAL NEWS','Local News'),
                ('WILDLIFE','Wildlife'),
                ('BANKING','Banking'),
                ('HOME','Home'),
                ('BOOKS','Books'),
                ('CARTOON','Cartoon'),
                ('OBITUARY','Obituary'),
                ('MUSIC AND MOVIES','Music and Movies'),
                ('OTHERS' , 'Others'))
    category=models.CharField(max_length=50, choices=feed_choices, default='current affairs')
    title = models.CharField(max_length=50)
    url=models.URLField()

# To return a user readable name
    def __str__(self):
        return self.title


class Article(models.Model):
    title=models.CharField(max_length=50)
    url=models.URLField()
    publication_date = models.DateTimeField()
    description=models.CharField(max_length=200)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

     #Delete all the article objects if the corresponding feed is deleted(one to many relationship)

    def __str__(self):
        return self.title
