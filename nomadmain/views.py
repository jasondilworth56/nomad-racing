from django.shortcuts import render, get_object_or_404
from nomadmain.models import Article, Media, TeamMember, StaticPage
from django.contrib.auth.models import User
from django.http import HttpResponse

import requests, random


TWITCH_CLIENT_ID = "fz19mrp6fjwd6qd7cueailm1qqq6za"
YOUTUBE_CLIENT_ID = "AIzaSyC8C1rkKpcwRP6yGRRSmHTXxiMP8LSJR3E"

NOMAD_TWITCH = "nomadsimracing"
NOMAD_YOUTUBE = "UCeO12ET3oRfa7zPcBUjj3rw"

def index(request):
    all_users = User.objects.all()
    users = []
    
    for user in all_users:
        if user.teammember.is_team():
            users.append(user)
    print("USERS BEFORE:",users)
    
    random.shuffle(users)
    print("USERS AFTER:", users)
    visible_users = users[:2]
    all_users = users
    
    articles = Article.objects.all()[:3]
    
    context = { 'visible_users': visible_users, 'all_users': all_users, 'live_stream': checkStreams(), 'articles': articles }
    return render(request, 'nomadmain/base.html', context)

def article_list(request):
    articles = Article.objects.all()
    if len(articles) > 0:
        main_image = articles[0].image
        context = { 'articles': articles, 'main_image': main_image.url,}
    else:
        context = {}
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
    random.shuffle(team_members)
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
    context = { 'live_stream' : checkStreams() }
    return render(request, 'nomadmain/live_now.html', context)

def result_list(request):
    return HttpResponse("Results")

def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug)
    context = { 'page' : page }
    return render(request, 'nomadmain/static_page.html', context)
        
def check_twitch(channel=NOMAD_TWITCH):
    twitch_request = "https://api.twitch.tv/kraken/streams/"+channel+"?client_id="+TWITCH_CLIENT_ID
    r = requests.get(twitch_request).json()
    stream = r['stream']
    return stream

def check_youtube(channel=NOMAD_YOUTUBE):
    youtube_request = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channel+"&type=video&eventType=live&key="+YOUTUBE_CLIENT_ID
    r = requests.get(youtube_request).json()
    return r

def checkStreams():
    team_members = TeamMember.objects.all()
    live_streams = []
    
    #check for NOMAD streams first
    stream = check_twitch()
    if stream != None:
        live_streams.append({'team_member':'NOMAD', 'embed':'https://player.twitch.tv/?channel='+NOMAD_TWITCH })
    r = check_youtube()
    if len(r['items']) > 0:
        live_streams.append({'team_member':'NOMAD', 'embed':'https://www.youtube.com/embed/'+r['items'][0]['id']['videoId']+'?rel=0'})
    
    if len(live_streams) == 0: #IF NOMAD STREAMS AREN'T LIVE, CHECK MEMBERS
        for team_member in team_members:
            if team_member.team_member:
                #CHECK FOR TWITCH CHANNEL
                if team_member.twitch_channel:
                    stream = check_twitch(team_member.twitch_channel)
                    if stream != None:
                        live_streams.append({'team_member':team_member, 'embed':'https://player.twitch.tv/?channel='+team_member.twitch_channel })
                
                #CHECK FOR YOUTUBE CHNNEL
                if team_member.youtube_channel:
                    r = check_youtube(team_member.youtube_channel)
                    if len(r['items']) > 0:
                        live_streams.append({'team_member':team_member, 'embed':'https://www.youtube.com/embed/'+r['items'][0]['id']['videoId']+'?rel=0'})
        
    if len(live_streams) > 0:
        return random.choice(live_streams)
    else:
        return None
        