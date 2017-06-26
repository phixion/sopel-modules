# sopel-modules
## Modules for Sopel IRC Bot

Requirements:

* [Sopel 6.x](https://github.com/sopel-irc/sopel/)
* [Python 3.3+](https://www.python.org/)

Contents:

* channel.py - channelmodule (BlizzCon/QuakeCon counters, reddit stuff, random youporn comments and more nonsense)
* streams.py - twitch.tv and hitbox.tv/smashcast.tv integration
* ud.py - adds .urban command to query [urbandictionary.com](http://urbandictionary.com)
* youtube.py - adds youtube APIv3.0 support to Sopel
* new_weather.py - fixes sopel's broken .wea command, also adds 7 day forecast (requires forecast.io and google url shortener API key)
* talk.py - adds .talk command (requires redis)
