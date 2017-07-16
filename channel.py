#!/usr/bin/python3
#encoding: utf-8

import sopel
from random import choice
import datetime
import requests
import re
import urllib.request as urllib2
import random

shrugs = [u"乁( ⁰͡ Ĺ̯ ⁰͡ ) ㄏ",
          u"¯\_(ツ)_/¯",
          u"¯\(º_o)/¯",
          u"┐(ツ)┌",
          u"¯\_( ͠° ͟ʖ °͠ )_/¯",
          u"ʅ(°_°)ʃ",
          u"┐(°,ʖ°)┌",
          u"¯\_(⌣̯̀ ⌣́)_/¯",
          u"¯\_(°ᴥ°)_/¯"]

@sopel.module.commands('quakecon')
def quakecon(bot, trigger):
   now = datetime.datetime.now()
   qcon = datetime.datetime(2017, 8, 4, 10)
   delta = qcon - now
   if delta.days < 6:
      hours, remainder = divmod(delta.seconds, 3600)
      minutes, seconds = divmod(remainder, 60)
      output = "{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until QuakeCon!".format(days=delta.days, hours=hours, minutes=minutes, seconds=seconds)
   else:
      output = "%s days until QuakeCon!" % delta.days
   bot.say(output)

@sopel.module.commands('blizzcon')
def blizzcon(bot, trigger):
   now = datetime.datetime.now()
   target = datetime.datetime(2017, 11, 3, 0)
   delta = target - now
   if delta.days < 7:
      hours, remainder = divmod(delta.seconds, 3600)
      minutes, seconds = divmod(remainder, 60)
      output = "{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until BlizzCon!".format(days=delta.days, hours=hours, minutes=minutes, seconds=seconds)
   else:
      output = "%s days until BlizzCon!" % delta.days
   bot.say(output)

@sopel.module.commands('zen')
def zen(bot, trigger):
   bot.say(requests.get("https://api.github.com/zen").text)

@sopel.module.commands('nfact')
def nfact(bot, trigger):
   bot.say(requests.get("http://numbersapi.com/random").text)

@sopel.module.commands('42')
def fourtytwo(bot, trigger):
   bot.say(requests.get("http://numbersapi.com/42").text)

@sopel.module.commands('tfact')
def today(bot, trigger):
   month = datetime.datetime.now().month
   day = datetime.datetime.now().day
   bot.say(requests.get("http://numbersapi.com/%s/%s/date" % (month, day)).text)

@sopel.module.commands('askreddit', 'asscredit')
def ask(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  bot.say(choice(requests.get("http://www.reddit.com/r/askreddit.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])

@sopel.module.commands('shower')
def shower(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  bot.say(choice(requests.get("http://www.reddit.com/r/showerthoughts.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])

@sopel.module.commands('5050')
def fifty(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/fiftyfifty.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s - %s" % (pick["title"], pick["url"]))

@sopel.module.commands('til', 'todayilearned')
def til(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/todayilearned.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["title"]))

@sopel.module.commands('kadse', 'kazachstan', 'c@', 'cat')
def kadse(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/catgifs.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["url"]))

@sopel.module.commands('livestreamfail', 'lsf', 'fail')
def lsf(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/LiveStreamFail.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["url"]))

@sopel.module.commands('aw', 'aww')
def aww(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/aww.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["url"]))

@sopel.module.commands('newbeat','latest')
def newbeat(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/beatheads/new.json?limit=1", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["url"]))

@sopel.module.commands('beat')
def beat(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/beatheads.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s" % (pick["url"]))

@sopel.module.commands('tifu')
def tifu(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  pick = choice(requests.get("http://www.reddit.com/r/tifu.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s - %s" % (pick["title"], pick["url"]))

@sopel.module.commands('rather')
def rather(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  bot.say(choice(requests.get("http://www.reddit.com/r/wouldyourather.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])

@sopel.module.commands('jpg','jpeg')
def jpg(bot, trigger):
   bot.say("Do I look like I know what a JPEG is? https://youtu.be/QEzhxP-pdos")

@sopel.module.commands('fap','fapathon')
def fap(bot, trigger):
   bot.say("https://i.imgur.com/9ciSNye.gifv")

@sopel.module.commands('rd')
def reverseDict(bot, trigger):
  word = trigger.group(2)
  if not word:
    bot.say("syntx: .rd <definition/description>")
  else:
    result = requests.get("http://api.datamuse.com/words", params={"rd": word}).json()
    if result:
      reply = "Possible words matching '%s': %s" % (word, ", ".join(w["word"] for w in result[0:5]))
      bot.say(reply)

@sopel.module.commands("lenny")
def lenny(bot, trigger):
  bot.say(u"( ͡° ͜ʖ ͡°)")

@sopel.module.commands("shrug")
def rand_shrug(bot, trigger):
   bot.say(u"%s" % (choice(shrugs)))

@sopel.module.commands("shrug1")
def shrug1(bot, trigger):
  bot.say(u"¯\_(ツ)_/¯")

@sopel.module.commands("shrug2")
def shrug2(bot, trigger):
  bot.say(u"¯\(º_o)/¯")

@sopel.module.commands("shrug3")
def shrug3(bot, trigger):
  bot.say(u"┐(ツ)┌")

@sopel.module.commands("wowalert")
def wowalert(bot, trigger):
    result = requests.get("http://status.wow-europe.com/en/alert").text
    pattern = re.compile('<.*?>')
    result = re.sub(pattern, '', result)
    bot.say(result)

@sopel.module.commands("free")
def free_software(bot, trigger):
  bot.say("https://p.hs.vc/u/free_software.gif")

@sopel.module.commands("hackes")
def hackes(bot, trigger):
   bot.say("THIS CHANNEL HAS BEEN HACKES!!!! ALL USERNAME THAT STAYED HERE FOR MORE THEN 300 SECONDS WILL AUTOMATICALLY RECEIVE A VT7.83 MICRO BUG THAT WILL DISABLE YOUR WINDOW SYSTEM EXCEPT WINDOW XP V1.03")

@sopel.module.rule(r'(^|.+ )hackes( .+|$)')
def hackes2(bot, trigger):
   bot.say("THIS CHANNEL HAS BEEN HACKES!!!! ALL USERNAME THAT STAYED HERE FOR MORE THEN 300 SECONDS WILL AUTOMATICALLY RECEIVE A VT7.83 MICRO BUG THAT WILL DISABLE YOUR WINDOW SYSTEM EXCEPT WINDOW XP V1.03")

@sopel.module.commands("invasion","invasions")
def invasion(bot, trigger):
  bot.say("https://wow.gameinfo.io/invasions")

@sopel.module.commands('doom')
def rather(bot, trigger):
  header =  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
  bot.say(choice(requests.get("http://www.reddit.com/r/MFDOOM_txt.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])
