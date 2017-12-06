from django.contrib import admin
from .models import TeamMember, Article, Media, Result, Progress

admin.site.register([TeamMember, Article, Media, Result])

# Register your models here.
