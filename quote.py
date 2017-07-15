from sopel import *
import random

qdb = "~/.sopel/quote.db"

@module.commands('addquote')
def addquote(bot, trigger):
        quote = trigger.group(2)
        f = open(qdb, 'a')
        f.write("\n%s" % quote)
        f.close()
        bot.reply('Your quote has been added!')

@module.commands('quote')
@module.example('.quote')
def quote(bot, trigger):
        f = open(qdb, 'r')
        line = random.choice(list(open(qdb)))
        bot.say(line)
