# coding=utf-8

from __future__ import unicode_literals, absolute_import, print_function, division
import requests
import sopel.module
from sopel.logger import get_logger
import re

LOGGER = get_logger(__name__)

yearfmt = re.compile('\((\d{4})\)')

@sopel.module.commands('movie', 'imdb')
@sopel.module.example('.movie ThisTitleDoesNotExist', '🎥 Movie not found!')
@sopel.module.example('.movie Citizen Kane', '🎥 Title: Citizen Kane | Year: 1941 | Rating: 8.4 | Genre: Drama, Mystery | IMDB Link: https://imdb.com/title/tt0033467')
def movie(bot, trigger):
    if not trigger.group(2):
        return
    word = trigger.group(2).rstrip()
    params={}

    # check to see if there is a year e.g. (2017) at the end
    last = word.split()[-1]
    if yearfmt.match(last) is not None:
        params['y'] = yearfmt.group(1)
        word = ' '.join(word.split[:-1])

    params['t'] = word
    bot.say(run_omdb_query(params, bot.config.core.verify_ssl, True))

def run_omdb_query(params, verify_ssl, add_url=True):
    uri = "https://www.omdbapi.com/?apikey=YOUR_API_KEY&t="
#    data = requests.get(uri, params={'t': word}, timeout=30,
#                        verify=bot.config.core.verify_ssl).json()
    data = requests.get(uri, params=params, timeout=30,
                        verify=verify_ssl).json()
    if data['Response'] == 'False':
        if 'Error' in data:
            message = '🎥 %s' % data['Error']
        else:
            LOGGER.warning(
                'Got an error from the OMDb api, search phrase was %s; data was %s',
                word, str(data))
            message = '🎥 Got an error from OMDbapi'
    else:
        message = '🎥 Title: ' + data['Title'] + \
                  ' | Year: ' + data['Year'] + \
                  ' | Rating: ' + data['imdbRating'] + \
                  ' | Genre: ' + data['Genre'] + \
                  ' | Plot: {}'
        if add_url:
            message += ' | IMDB Link: https://imdb.com/title/' + data['imdbID']

        plot = data['Plot']
        if len(message.format(plot)) > 300:
            cliplen = 300 - (len(message) - 2 + 3) # remove {} add […]
            plot = plot[:cliplen]

    return message.format(plot)

@sopel.module.rule('.*(imdb\.com\/title\/)(tt[0-9]+).*')
def imdb_url(bot,trigger,found_match=None):
    match = found_match or trigger
    bot.say(run_omdb_query({'i': match.group(2)},
                            bot.config.core.verify_ssl, False))

if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
