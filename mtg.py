import requests
import json
import sopel

@sopel.module.commands('mtg','magic')
def mtg(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    i = trigger.group(2)
    x = requests.get('https://api.deckbrew.com/mtg/cards?name={0}'.format(i))
    c = x.json()
    if not c:
        return bot.say('Card not found.')
    js = c[0]
    if 'creature' in js['types']:
        if 'power' in js:
            bot.say('Name: {0}, Type: {1}, Cost: {2}, Effect: {3}, Power: {4}, Toughness: {5}'.format(js['name'], js['types'], js['cost'], js['text'], js['power'], js['toughness']))
        else:
            bot.say('Name: {0}, Type: {1}, Cost: {2}, Effect: "{3}"'.format(js['name'], js['types'], js['cost'], js['text']))
    else:
        bot.say('Name: {0}, Type: {1}, Cost: {2}, Effect: "{3}"'.format(js['name'], js['types'], js['cost'], js['text']))
