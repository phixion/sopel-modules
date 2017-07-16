import sopel
import requests

@sopel.module.commands('yp')
def youporn(bot, trigger):
  search_for = trigger.group(2)
  header = {'accept': 'application/json'}
  rpc = requests.get("https://porncomment.com",{'search': search_for}, headers=header).json()["comments"]
  comment = rpc[0]['body']
  bot.say(comment, max_messages=2)
  