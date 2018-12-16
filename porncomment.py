import sopel
import requests

@sopel.module.commands('yp')
@sopel.module.example('.yp trump')
def porncomment(bot, trigger):
  search_for = trigger.group(2)
  header = {'accept': 'application/json'}
  try:
    rpc = requests.get("https://porncomment.com",{'search': search_for}, headers=header).json()["comments"]
    comment = rpc[0]['body']
    bot.say(comment, max_messages=2)
  except IndexError:
    bot.say("no comment found :(")
      
@sopel.module.commands('ypurl')
@sopel.module.example('.ypurl trump')
def porncomment_url(bot, trigger):
  search_for = trigger.group(2)
  header = {'accept': 'application/json'}
  try:
    rpc = requests.get("https://porncomment.com",{'search': search_for}, headers=header).json()["comments"]
    comment = rpc[0]['body']
    url = rpc[0]['source_url']
    full_comment = '%s - %s' %(comment, url)
    bot.say(full_comment, max_messages=2)
  except IndexError:
    bot.say("no comment found :(")
