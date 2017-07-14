#!/usr/bin/python3
"""
urbandict.py - urban dictionary module
much cleaner, TODO bring random urban back
"""

import sopel.web as web
import json
import sopel

@sopel.module.commands('urban')
@sopel.module.example('.urban beat head')
def urbandict(bot, trigger):
    """.urban <word> - Search Urban Dictionary for a definition."""

    word = trigger.group(2)
    if not word:
        return bot.say(urbandict.__doc__.strip())

    try:
        data = web.get("http://api.urbandictionary.com/v0/define?term={0}".format(web.quote(word)))
        data = json.loads(data)
    except:
        return bot.say("Error connecting to urban dictionary")

    if data['result_type'] == 'no_results':
        return bot.say("No results found for {0}".format(word))

    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(
        web.quote(word))

    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    bot.say(response)

if __name__ == '__main__':
    print(__doc__.strip())

