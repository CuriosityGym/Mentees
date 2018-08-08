# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
# Creates an app so that it can be used in the project
# It is included in settings.py so that Django knows it has to be included in the project
class NewsConfig(AppConfig):
    name = 'news'
