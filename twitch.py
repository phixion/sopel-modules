#As of 09-14-2016, twitch API now requires Client-ID with all requests.  You will need to create one from here: 
# https://www.twitch.tv/settings/connections
# complete twitch.py rewrite coming soon™
import requests
import sopel
import re
from sopel.tools import SopelMemory
import datetime

# TODO: Make these config options c:
twitchclientid = "YOUR_API_KEY" 
announce_chan = "#pony.ql"
logchannel = "#willie-testing" #used for live logging certain issues that plague this module
streamers = [
  "phixxion",
  "hc_mikle",
  "beatheadstv",
  "ijustwantagf",
  "h3h3productions",
  "quakecon",
  "dreamhackql",
  "runterfallnoob",
  "gamesdonequick",
  "mikletv",
  "freddurst",
  "carkasjak",
  "blizzard",
  "scglive",
  "linustech",
  "quakecon",
  "lofihiphop",
  "awesomehardware",
  "ridelore",
  "luke_lafr",
  "jonmakesbeats",
  "quakechampions",
  "warcraft",
  "iverass",
  "grandpoobear",
  "esamarathon",
  "zibbsi",
  "back2warcraft",
  "thedivisiongame",
  "aws"
]

twitchregex = re.compile('(?!.*\/v\/).*https?:\/\/(?:www\.)?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][twitchregex] = twitchirc


def shutdown(bot):
    del bot.memory['url_callbacks'][twitchregex]

currently_streaming = {}

@sopel.module.interval(20)
def monitor_streamers(bot):
  streaming_names = []
  try:
    streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(streamers)}, headers={"Client-ID":twitchclientid}).json()
  except Exception as  e:
    return print("There was an error reading twitch API  {0}".format(e))
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_url = streamer["channel"]["url"]
      streamer_status = streamer["channel"]["status"]
      streamer_starttime = datetime.datetime.strptime(streamer['created_at'], '%Y-%m-%dT%H:%M:%SZ')
      streamer_viewers = streamer["viewers"]
      
      if streamer_name not in currently_streaming:
        currently_streaming[streamer_name] = streamer_game, {'cooldown': 0, 'starttime': streamer_starttime}
        results.append("🕹️ %s just went live playing %s! %s - %s" % (streamer_name,streamer_game,streamer_status,streamer_url))
      
      streaming_names.append(streamer_name)

  if results:
    bot.msg(announce_chan, ", ".join(results))  

  # Remove people who stopped streaming
  for streamer in list(currently_streaming):
    if streamer not in streaming_names:
      currently_streaming[streamer][1]['cooldown'] += 10
    if currently_streaming[streamer][1]['cooldown'] > 130:
      bot.msg(logchannel,'{0} was removed from currently_streaming for reaching a cooldown of {1}'.format(streamer,currently_streaming[streamer][1]['cooldown']))
      del currently_streaming[streamer]

@sopel.module.commands('twitch','stream')
@sopel.module.example('.twitch  or .stream username')
def streamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}, headers={"Client-ID":twitchclientid}).json()
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_url = streamer["channel"]["url"]
      streamer_status = streamer["channel"]["status"]
      streamer_viewers = streamer["viewers"]
    
      results.append("🕹️ %s is playing %s %s - %s - %s viewer%s" % (streamer_name, 
                                                           streamer_game, 
                                                           streamer_url,
                                                           streamer_status, 
                                                           streamer_viewers, 
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    bot.say("🕹️ nobody is currently streaming.")

@sopel.module.rule('(?!.*\/v\/).*https?:\/\/(?:www\.)?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')
def twitchirc(bot, trigger, match = None):
  match = match or trigger
  streamer_name = match.group(1)
  query = streamers if streamer_name is None else streamer_name.split(" ")
  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}, headers={"Client-ID":twitchclientid}).json()
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_status = streamer["channel"]["status"]
      streamer_viewers = streamer["viewers"]

      results.append("🕹️ %s is playing %s [%s] - %s viewer%s" % (streamer_name,
                                                           streamer_game,
                                                           streamer_status,
                                                           streamer_viewers,
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    pass
    #bot.say("Nobody is currently streaming.")

@sopel.module.commands('debugtv')
def debug(bot, trigger):
    bot.msg(logchannel,"currently_streaming: {}".format(", ".join(currently_streaming)))

@sopel.module.rule('.*(?:https?:\/\/clips\.twitch.tv\/(.*?)\/?(?:(?=[\s])|$))|(?:https?:\/\/(?:www)?\.twitch\.tv\/.*?\/clip\/(.*?)\/?(?:(?=[\s])|$))')
def twitchclipsirc(bot,trigger, match = None):
  match = match or trigger
  slug = match.group(1) or match.group(2)
  clips = requests.get("https://api.twitch.tv/kraken/clips/{}".format(slug),
  headers={"Client-ID":twitchclientid,"Accept":"application/vnd.twitchtv.v5+json"}).json()
  name = clips['broadcaster']['display_name']
  title = clips['title']
  game = clips['game']
  views = clips['views']
  bot.say("🕹️ {} [{}] | {} | {} views".format(title, game, name, views))

@sopel.module.commands('debugtv')
def debug(bot, trigger):
    bot.msg(logchannel,"currently_streaming: {}".format(", ".join(currently_streaming)))
