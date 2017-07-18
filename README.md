[![Build Status](https://travis-ci.org/phixion/sopel-modules.svg?branch=master)](https://travis-ci.org/phixion/sopel-modules)

# sopel-modules



### Requirements:

* [Sopel 6.x](https://github.com/sopel-irc/sopel/)
* [Python 3.5](https://www.python.org/)

### Prerequisites:

```
pip install -r requirements.txt
```
remove 'sopel' if you build from a different source


### Installation

[Clone this repository](https://help.github.com/articles/cloning-a-repository/) and [edit your bot's configfile to load modules from that directory](https://sopel.chat/docs/config.html#sopel.config.core_section.CoreSection.extra)


### API Keys:

* [youtube](https://console.developers.google.com/)
* [google maps traffic](https://console.developers.google.com/)
* [google url shortener](https://console.developers.google.com/)
* [darksky (formerly forecast.io)](https://darksky.net/dev/)
* [soundcloud](https://developers.soundcloud.com/)
* [twitch](https://www.twitch.tv/settings/connections)


### Contents:

* channel.py - channelmodule (BlizzCon/QuakeCon counters, reddit stuff, actually a lot of nonsense)
* twitch.py - twitch.tv and hitbox.tv integration (info when link is posted, channel announcement when stream goes online)
* ud.py - adds .urban command to query [urbandictionary.com](http://urbandictionary.com)
* youtube.py - adds youtube APIv3.0 support to Sopel (requires API key)
* forecast.py - fixes sopels broken .weather command (requires darksky.net and google url shortener API key)
* talk.py - adds .talk command
* gdq - adds .gdq command which returns days until AGDQ starts + basic shedule of upcoming games
* howlongtobeat.py - adds .hltb command which would return the playtime of a game from howlongtobeat.com
* hots.py - returns most famous buildorders based on hotslogs.com
* mtg.py - basic lookup for magic the gathering cards
* traffic.py - returns duration for a trip by a predefined vehicle (requires api key)
* quote.py - very basic quote database
* imdb.py - returns info to imdb links and adds .imdb command to search
* vimeo.py - returns information to vimeo links
* cur.py - currency conversion and btc
* dubtrack.py - returns the currently played song on beatheads dubtrack channel
* sc.py - returns information to soundcloud links (tracks and playlist) (requires API key)
* porncomment.py - returns a random porncomment if no searchterm is provided
* tvmaze.py - looks up a tvshow's airing time and date using tvmaze api


### Thanks:

* [dasu](https://github.com/dasu) as most of the modules are based on his

