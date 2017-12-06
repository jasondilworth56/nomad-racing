from django.db import models

# Create your models here.


#A member of the NOMAD team
class TeamMember(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    iRacing_number = models.CharField(max_length=10)
    profile_photo = models.FileField()
    date_of_birth = models.DateField()
    biography = models.TextField()
    twitch_channel = models.CharField(max_length=30)
    youtube_channel = models.CharField(max_length=30)
    personal_site = models.CharField(max_length=255)


#An Article on the blog/news
class Article(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField()
    content = models.TextField()
    category = models.CharField(max_length=255) #TODO: Add categories class, this should be a foreign field of that
    timestamp = models.DateTimeField(auto_now=True)
    team_members = models.ManyToManyField(TeamMember) #for tagging team members
    
#A piece of media
class Media(models.Model):
    filename = models.FileField()
    team_members = models.ManyToManyField(TeamMember) #for tagging team members
    
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
    
class Progress(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    iRating = models.IntegerField()
