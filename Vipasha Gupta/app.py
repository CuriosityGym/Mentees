apps.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
# Creates an app so that it can be used in the project
# It is included in settings.py so that Django knows it has to be included in the project
class NewsConfig(AppConfig):
    name = 'news'

urls.py-newsproject

"""newsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Checks if the URL begins with admin then redirects it to that site
    url(r'^news/', include('news.urls')),
    # Checks if the URL begins with news
    # Redirects it to news.urls.py where it is redirected according to the URL
]


urls.py-news


from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.articles_list, name='articles_list'),
    # Checks if the URL contains only /news
    # If it matches then redirects it to articles_list
    url(r'^feeds/new', views.new_feed, name='feed_new'),
    url(r'^feeds/', views.feeds_list, name='feeds_list'),
]
views.py

from django.shortcuts import render # Acts as a middleman between request and response
from .models import Article, Feed
from .forms import FeedForm, CategoryForm # To import a form to allow a form to be created for user to input data
from django.shortcuts import redirect
import feedparser # To assist filtering out the RSS feed to give articles
import datetime
from django.http import HttpResponse
from django.db.models import F

# Create your views here.

def articles_list(request):
   
        articles = Article.objects.all()
        # Recieves all the objects from the article database from models.py
        rows = [articles[x:x+1] for x in range(0, len(articles), 1)]
        # To assist in displaying the articles two in a row
        return render(request, 'news/articles_list.html', {'rows': rows})
        # Redirects the request to articles_list.html and passes 'rows' as a key and rows as a variable
        # Returns the response to the user

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})

def new_feed(request):
    if request.method == "POST":
        # Only if the HTML request is of the POST type then accept the URL
        form = FeedForm(request.POST)
        if form.is_valid():
            # If it is a valid URL then save the URL
            feed = form.save(commit=False)
            # Commit ensures its not stored in the database yet but stored in the memory
            # Used to change something(title in this case)
            existingFeed = Feed.objects.filter(url = feed.url)
            # Checking if the feed URL already exists in the database
            # To avoid duplicate feeds
            if len(existingFeed) == 0:
                feedData = feedparser.parse(feed.url)
                # Convert the given data to a readable format
            else:
                response='The URL already exists'
                return render(request,'news/failed.html' , {'response':response})
                # To inform the user if the URL entered already exists
                # set some fields
            feed.title = feedData.feed.title
            # Save the title of the feed
            feed.save()
                # Save it in the database which is defined in models.py

            for entry in feedData.entries:
                    # Running a loop to access all the articles in the feed
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description
                    d =datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')
                    # Converting the date to the required format(DateTimeField)
                    article.publication_date = dateString
                    article.feed = feed
                    article.save()

            return redirect('news.views.feeds_list')
            # Redirects it to views.feeds_list to display the feeds

    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})

        # First form that the user views which redirects here
    # If it is invalid it doesn't save the form

articles_list.html

<!--This template handles the displaying of all the articles-->
{% extends 'news/base.html' %}

{% block content %}

<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="jumbotron">
  <div class="container">
    <h1>Django News</h1>
    <p>Have a look around to see some of the latest and greatest news articles from your favorite feeds.</p>
  </div>
</div>

<div class="container">
  <style>
p {
  border-style: hidden;
}
</style>
<!--Used to assist in neat display-->
<form method="post">
  <!--To accept the form in the form of a POST http request-->
  {% csrf_token %}
  <!-- To ensure security-->
{{ category_form.as_p }}
<!--accepts the value as a paragraph-->
<hr>
<!--Draw a horizontal line-->
</form>

{% for row in rows %}
  <!--Runs for loop in the rows array to access articles in twos-->
    <div class="col-md-6">
    <!--Used to display articles two in a row-->
      {% for entry in row %}
    <!--Runs for loop in the row array to access articles one by one-->
        <h2>{{entry.title}}</h2>
        <p>{{entry.description | safe}}</p>
           <!--Reassures HTML that it can use some other HTML souce-->
        <p><a href="{{entry.url}}" target="_blank" class="btn btn-primary">View Details</a></p><p></p>
          <!--Creates a link to redirect the user to another page to view the article in detail-->
      {% endfor %}
    <hr>
    </div>
{% endfor %}

<!-- Creates a footer -->
  <footer>
    <p>&copy; 2018 Django News Aggregator</p>
  </footer>
</div> <!-- /container -->
{% endblock %}

failed.html

{% extends 'news/base.html' %}
{% block content %}
<div class="jumbotron">
  <div class="container">
    <hr>
    <p>  {{response}} </p>

{% endblock %}

new_feed.html

<!--This template accepts forms from the user and saves them-->
{% extends 'news/base.html' %}
<!-- Takes the code from base.html(to prevent redundant coding) and then has its own individual function-->
{% block content %}
<!--This allows us to add things from elsewhere
                          and allow the inherited template to make changes to the base template-->
<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="jumbotron">
  <div class="container">
    <!--Div defines this part of the code as the container--->
<form method="post">
  <!--To accept the form in the form of a POST http request-->
  {% csrf_token %}
  <!-- To ensure security-->
{{ form.as_p }}
<!--accepts the value as a paragraph-->
<hr>
<!--Draw a horizontal line-->
<button type="submit" class="btn btn-primary">Save</button>

<!--Form to accept the URL from the user-->
</form>
{% endblock %}

feed_list.html

{% extends 'news/base.html' %}

{% block content %}

<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="jumbotron">
  <div class="container">
    <h1>News Feeds</h1>
  </div>
</div>

<div class="container">
<a href="{% url 'feed_new' %}" class="btn btn-primary">New Feed</a>
<!--Once new feed button is clicked it takes the URL and passes it to urls.py which passes it to views-->
<hr>
  <ul>
    {% for feed in feeds %}
      <li><a href="{{feed.url}}">{{feed.title}}</a></li>
    {% endfor %}
  </ul>

  <footer>
    <p>&copy; 2018 Django News Aggregator</p>
  </footer>
</div> <!-- /container -->

{% endblock %}

base.html

 <!--Template which is the base and has the basic code that is needed for display -->
<!DOCTYPE html>
<html lang="en">
  <head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Django News Aggregator</title>

    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
  </head>

  <body>
    <!--Creates a navigation bar which allows the user to move from one part of the page to the other-->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Django New Aggregator</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="{% url 'articles_list' %}">Home</a></li>
            <!--Redirects to articles_list when home is clicked-->
            <li><a href="{% url 'feeds_list' %}">Feeds</a></li>
            <!--Redirects to feeds_list when Feeds is clicked-->
          </ul>
        </div>
      </div>
    </nav>

    {% block content %}
    {% endblock %}

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  </body>
</html>

models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Importing to sublclass(inheriting) models
# Create your models here.
class Feed(models.Model):
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


forms.py

from django import forms
from .models import Feed

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        # Django knows which model it has to take fields from
        fields = ['url','category']
        # Extracts that field from the specified model

admin.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Feed, Article
# Register your models here.
admin.site.register(Feed)
admin.site.register(Article)
# If the URL /admin is opened the registered articles and feeds will be displayed


settings.py
    
"""
Django settings for newsproject project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't(m%9w=rt0poms7-))=)028)((#rg2x&h(i@@89ugqvh6opb91'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'news.apps.NewsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsproject.urls'

TEMPLATES = [
   {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
