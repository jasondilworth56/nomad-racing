from django.shortcuts import render
from nomadmain.models import Article, Media, TeamMember

import requests, random

TWITCH_CLIENT_ID = "fz19mrp6fjwd6qd7cueailm1qqq6za"
YOUTUBE_CLIENT_ID = "AIzaSyC8C1rkKpcwRP6yGRRSmHTXxiMP8LSJR3E"

def index(request):
    team_members = TeamMember.objects.all()
    articles = Article.objects.all()[:3]
    
    
    context = { 'team_members': team_members, 'live_stream': checkStreams(), 'articles': articles }
    return render(request, 'nomadmain/index.html', context)

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
        