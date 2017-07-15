# willie-modules
## Modules for Sopel IRC Bot

Requirements:

* [Sopel 6.x](https://github.com/sopel-irc/sopel/)
* [Python 3.x](https://www.python.org/)

Contents:

* channel.py - channelmodule (BlizzCon/QuakeCon counters, reddit queries, random youporn comments and more nonsense)
* twitch.py - twitch.tv and hitbox.tv integration (API query, channel announcement when stream goes online)
* ud.py - adds .urban command to query [urbandictionary.com](http://urbandictionary.com)
* youtube.py - adds youtube APIv3.0 support to Sopel (requires API key)
* forecast.py - fixes sopels broken .weather command (requires forecast.io and google url shortener API key)
* talk.py - adds .talk command (requires redis)
* gdq - adds .gdq command which returns days until AGDQ starts + basic shedule of upcoming games
* howlongtobeat.py - adds .hltb command which would return the playtime of a game from howlongtobeat.com
* hots.py - returns most famous buildorders based on hotslogs.com
* mtg.py - basic lookup for magic the gathering cards
* traffic.py - returns duration for a trip by a predefined vehicle (based on gmaps api, requires api key)
* quote.py - very basic quote database
* imdb.py - returns info to imdb links and adds .imdb command to search
* vimeo.py - returns information to vimeo links
* cur.py - currency conversion and btc
* dubtrack.py - returns the currently played song on beatheads dubtrack channel