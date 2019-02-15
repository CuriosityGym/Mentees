# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Feed, Article
# Register your models here.
admin.site.register(Feed)
admin.site.register(Article)
# If the URL /admin is opened the registered articles and feeds will be displayed
