from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# A member of the NOMAD team
class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iRacing_number = models.CharField(max_length=10, null=True, blank=True)
    profile_photo = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    twitch_channel = models.CharField(max_length=30, null=True, blank=True)
    youtube_channel = models.CharField(max_length=30, null=True, blank=True)
    personal_site = models.CharField(max_length=255, null=True, blank=True)
    team_member = models.BooleanField(default=False)
    slug = models.SlugField(max_length=60, blank=True)
    
    def get_full_name(self):
        return self.user.get_full_name()
        
    def is_team(self):
        return self.team_member
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_full_name())

        super(TeamMember, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TeamMember.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.teammember.save()

class ArticleCategory(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name
    
# A piece of media
class Media(models.Model):
    filename = models.FileField()
    team_members = models.ManyToManyField(TeamMember) #for tagging team members in media
    
    def __str__(self):
        return self.filename.name
    
# An Article on the blog/news
class Article(models.Model):
    slug = models.SlugField(max_length=60, blank=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE) #TODO: Add categories class, this should be a foreign field of that
    timestamp = models.DateTimeField(auto_now=True)
    team_members = models.ManyToManyField(TeamMember, blank=True) #for tagging team members in articles
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Article, self).save(*args, **kwargs)
    
# A result of a team member
class Result(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    series = models.CharField(max_length=60)
    circuit = models.CharField(max_length=128)
    race_type = models.CharField(max_length=30)
    start_pos = models.IntegerField()
    finish_pos = models.IntegerField()
    iRating_change = models.IntegerField()
    
# A store of iRatings of each TeamMember each day
class Progress(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    iRating = models.IntegerField()

# A static page model for CRM usage
class StaticPage(models.Model):
    slug = models.SlugField(max_length=60, blank=True)
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super (StaticPage, self).save(*args, **kwargs)