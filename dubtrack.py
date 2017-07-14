import requests
import sopel
import json

@sopel.module.commands('dt','beats')
def djpoi(bot,trigger):
    #bot.say("")
    x = requests.get("http://api.dubtrack.fm/room/58fa285f78c3bfb500a1dff2").json()
    if not x['data']['currentSong']:
        bot.say("join at https://www.dubtrack.fm/join/spzo")
    else:
        bot.say("Current song: {0} | https://www.dubtrack.fm/join/spzo".format(x['data']['currentSong']['name'],x['data']['activeUsers']))
