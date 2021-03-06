from django.contrib import admin
from .models import TeamMember, Article, Media, Result, Progress, ArticleCategory, StaticPage
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, SelectMultiple
from django.db import models

admin.site.site_header = admin.site.site_title = "NOMAD Sim Racing"
admin.site.index_title = ""

admin.site.register([Media, Result, StaticPage])

# Register your models here.
   
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'title', 'get_category')
    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = "Category"
    
    list_filter = ['timestamp']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style':'width:515px;'})},
        models.TextField: {'widget': Textarea(attrs={'style':'width:515px;'})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'style':'width:530px;'})}
    }
    
    prepopulated_fields = {"slug": ("title",)}

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    can_delete = False
    verbose_name_plural = 'Team Member'
    fk_name = 'user'
    

 
class CustomUserAdmin(UserAdmin):
    inlines = (TeamMemberInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_team_member')
    list_select_related = ('teammember', )
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_team_member(self, obj):
        return obj.teammember.team_member
    get_team_member.short_description = "Team Member"
    get_team_member.boolean = True
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)