from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *
# Register your models here.
admin.site.register(movie_detail)
admin.site.register( WatchLater)
admin.site.register(UserProfile)
admin.site.register(Session)
