#!/usr/bin/python3

import requests
import sopel

@sopel.module.commands('urban')
@sopel.module.example('.urban beat head')
def urbandict(bot, trigger):
    word = trigger.group(2)
    if not word:
        return bot.say(urbandict.__doc__.strip())
    try:
        data = requests.get("http://api.urbandictionary.com/v0/define?term={0}".format(requests.utils.quote(word))).json()
    except:
        return bot.say("Error connecting to urban dictionary")

    if not data['list']:
        return bot.say("No results found for {0}".format(word))
    try:
        result = list(filter(lambda x: x['word'].lower() == word.lower(), data['list']))[0]
    except:
        return bot.say("No results found for {0}".format(word))
    url = 'http://{}.urbanup.com'.format(word.replace(' ','-'))
    maxdesc = 420 - len(url)
    response = "{0} - {1}".format((result['definition'].replace("[","").replace("]","").strip()[:maxdesc])+"...", url)
    bot.say(response)

if __name__ == '__main__':
    print(__doc__.strip())
