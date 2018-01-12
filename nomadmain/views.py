from django.shortcuts import render, get_object_or_404
from nomadmain.models import Article, Media, TeamMember
from django.contrib.auth.models import User
from django.http import HttpResponse

import requests, random

TWITCH_CLIENT_ID = "fz19mrp6fjwd6qd7cueailm1qqq6za"
YOUTUBE_CLIENT_ID = "AIzaSyC8C1rkKpcwRP6yGRRSmHTXxiMP8LSJR3E"

def index(request):
    all_users = User.objects.all()
    users = []
    
    for user in all_users:
        if user.teammember.is_team():
            users.append(user)
    
    articles = Article.objects.all()[:3]
    
    context = { 'users': users, 'live_stream': checkStreams(), 'articles': articles }
    return render(request, 'nomadmain/base.html', context)

def article_list(request):
    articles = Article.objects.all()
    main_image = articles[0].image
    context = { 'articles': articles, 'main_image': main_image.url,}
    return render(request, 'nomadmain/base_articles.html', context)

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = { 'article': article }
    return render(request, 'nomadmain/base_article.html', context)

def team_list(request):
    users = User.objects.all()
    team_members = []
    for user in users:
        if user.teammember.team_member == True:
            team_members.append(user)
    
    context = { 'team_members': team_members }
    return render(request, 'nomadmain/base_team_members.html', context)

def team_member(request, slug):
    team_member = get_object_or_404(TeamMember, slug=slug)
    user = team_member.user
    
    context = {'user':user}
    return render(request, 'nomadmain/base_team_member.html', context)
    
def events(request):
    return HttpResponse("Events")

def live_now(request):
    return HttpResponse("Live Now")

def result_list(request):
    return HttpResponse("Results")
        

def checkStreams():
    team_members = TeamMember.objects.all()
    live_streams = []
    for team_member in team_members:
        if team_member.team_member:
            #CHECK FOR TWITCH CHANNEL
            if team_member.twitch_channel:
                twitch_request = "https://api.twitch.tv/kraken/streams/"+team_member.twitch_channel+"?client_id="+TWITCH_CLIENT_ID
                r = requests.get(twitch_request).json()
                stream = r['stream']
                if stream != None:
                    live_streams.append({'team_member':team_member, 'embed':'https://player.twitch.tv/?channel='+team_member.twitch_channel })
            
            #CHECK FOR YOUTUBE CHNNEL
            if team_member.youtube_channel:
                youtube_request = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+team_member.youtube_channel+"&type=video&eventType=live&key="+YOUTUBE_CLIENT_ID
                r = requests.get(youtube_request).json()
                if len(r['items']) > 0:
                    live_streams.append({'team_member':team_member, 'embed':'https://www.youtube.com/embed/'+r['items'][0]['id']['videoId']+'?rel=0'})
    
    if len(live_streams) > 0:
        return random.choice(live_streams)
    else:
        return None
        