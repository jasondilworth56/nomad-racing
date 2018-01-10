from django.contrib import admin
from .models import TeamMember, Article, Media, Result, Progress, ArticleCategory

admin.site.register([Media, Result])

# Register your models here.
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'team_member')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'title', 'get_category')
    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = "Category"
    
    list_filter = ['timestamp']
    
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)