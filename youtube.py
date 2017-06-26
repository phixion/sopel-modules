# coding=utf8
"""Youtube module for Sopel"""
from __future__ import unicode_literals, division

from sopel.module import rule, commands, example
from sopel.config.types import StaticSection, ValidatedAttribute, NO_DEFAULT
from sopel.formatting import color, colors
from sopel import tools
import datetime
import sys
import re
import apiclient.discovery
if sys.version_info.major < 3:
    int = long

ISO8601_PERIOD_REGEX = re.compile(
    r"^(?P<sign>[+-])?"
    r"P(?!\b)"
    r"(?P<y>[0-9]+([,.][0-9]+)?(?:Y))?"
    r"(?P<mo>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<w>[0-9]+([,.][0-9]+)?W)?"
    r"(?P<d>[0-9]+([,.][0-9]+)?D)?"
    r"((?:T)(?P<h>[0-9]+([,.][0-9]+)?H)?"
    r"(?P<m>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<s>[0-9]+([,.][0-9]+)?S)?)?$")
regex = re.compile('(youtube.com/watch\S*v=|youtu.be/)([\w-]+)')
API = None


class YoutubeSection(StaticSection):
    api_key = ValidatedAttribute('api_key', default=NO_DEFAULT)
    """The Google API key to auth to the endpoint"""


def configure(config):
    config.define_section('youtube', YoutubeSection, validate=False)
    config.youtube.configure_setting(
        'api_key',
        'Enter your Google API key.',
    )


def setup(bot):
    bot.config.define_section('youtube', YoutubeSection)
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = get_info
    global API
    API = apiclient.discovery.build("youtube", "v3",
                                    developerKey=bot.config.youtube.api_key)


def shutdown(bot):
    del bot.memory['url_callbacks'][regex]


@commands('yt', 'youtube')
@example('.yt h3h3productions rekt together')
def search(bot, trigger):
    """Search YouTube"""
    if not trigger.group(2):
        return
    results = API.search().list(
        q=trigger.group(2),
        type='video',
        part='id,snippet',
        maxResults=1,
    ).execute()
    results = results.get('items')
    if not results:
        bot.say("I couldn't find any YouTube videos for your query.")
        return

    _say_result(bot, trigger, results[0]['id']['videoId'])


@rule('.*(youtube.com/watch\S*v=|youtu.be/)([\w-]+).*')
def get_info(bot, trigger, found_match=None):
    """
    Get information about the latest video uploaded by the channel provided.
    """
    match = found_match or trigger
    _say_result(bot, trigger, match.group(2), include_link=False)


def _say_result(bot, trigger, id_, include_link=True):
    result = API.videos().list(
        id=id_,
        part='snippet,contentDetails,statistics',
    ).execute().get('items')
    if not result:
        return
    result = result[0]

    message = (
        '[YouTube] '
        '{title} | Uploader: {uploader} | '
        'Length: {length} | Views: {views:,}'
    )

    snippet = result['snippet']
    details = result['contentDetails']
    statistics = result['statistics']
    duration = _parse_duration(details['duration'])
    uploaded = _parse_published_at(bot, trigger, snippet['publishedAt'])
    comments = statistics.get('commentCount', '-')
    if comments != '-':
        comments = '{:,}'.format(int(comments))

    message = message.format(
        title=snippet['title'],
        uploader=snippet['channelTitle'],
        length=duration,
        uploaded=uploaded,
        views=int(statistics['viewCount']),
        comments=comments,
    )
    if 'likeCount' in statistics:
        likes = int(statistics['likeCount'])
        message += ' | ' + color('{:,}+'.format(likes), colors.GREEN)
    if 'dislikeCount' in statistics:
        dislikes = int(statistics['dislikeCount'])
        message += ' | ' + color('{:,}-'.format(dislikes), colors.RED)
    if include_link:
        message = message + ' | Link: https://youtu.be/' + id_
    bot.say(message)


def _parse_duration(duration):
    splitdur = ISO8601_PERIOD_REGEX.match(duration)
    dur = []
    for k, v in splitdur.groupdict().items():
        if v is not None:
            dur.append(v.lower())
    return ' '.join(dur)


def _parse_published_at(bot, trigger, published):
    pubdate = datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%S.%fZ')
    return tools.time.format_time(bot.db, bot.config, nick=trigger.nick,
        channel=trigger.sender, time=pubdate)
