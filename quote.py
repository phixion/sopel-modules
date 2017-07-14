from sopel import *
import random

qdb = "/home/bot/.willie/quote.db"

@module.commands('addquote')
def addquote(bot, trigger):
        quote = trigger.group(2)
        f = open(qdb, 'a')
        f.write("\n%s" % quote)
        f.close()
        bot.reply('quote added boiiii')

@module.commands('quote')
@module.example('.quote')
def quote(bot, trigger):
        f = open(qdb, 'r')
        line = random.choice(list(open(qdb)))
        bot.say(line)
