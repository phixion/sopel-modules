# coding=utf-8

from __future__ import unicode_literals, absolute_import, print_function, division
import requests
import json
from sopel.module import commands, example, NOLIMIT
from datetime import datetime
from pytz import timezone

forecastapi = 'YOUR_API_KEY' #forecast.io API key.
gurlapi = 'YOUR_API_KEY' #google url shortner api key

def get_short_url(gurl):
    global gurlapi
    short_url_service = 'https://www.googleapis.com/urlshortener/v1/url?key={0}'.format(gurlapi)
    payload = {'longUrl': gurl}
    headers = {'content-type': 'application/json'}
    r = requests.post(short_url_service, data=json.dumps(payload), headers=headers)
    return r.json()['id']

def woeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where text="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

def reversewoeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where woeid="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

def get_temp(forecast):
    try:
        temp = round(forecast.json()['currently']['temperature'])
        app_temp = round(forecast.json()['currently']['apparentTemperature'])
    except (KeyError, ValueError):
        return 'unknown'
    high = round(forecast.json()['daily']['data'][0]['temperatureMax'])
    low = round(forecast.json()['daily']['data'][0]['temperatureMin'])
    if forecast.json()['flags']['units'] == 'us':
        if temp == app_temp:
            return (u'%d\u00B0F (H:%d|L:%d)' % (temp, high, low))
        else:
            return (u'%d\u00B0F, (App:%d, H:%d|L:%d)' % (temp, app_temp, high, low))
    else:
        if temp == app_temp:
            return (u'%d\u00B0C (H:%d|L:%d)' % (temp, high, low))
        else:
            return (u'%d\u00B0C, (App:%d, H:%d|L:%d)' % (temp, app_temp, high, low))

def get_uv(postal):
    try:
        uvreq = requests.get("https://iaspub.epa.gov/enviro/efservice/getEnvirofactsUVHOURLY/ZIP/{}/JSON".format(postal)).json()
    except:
        return ''
    now = datetime.now()
    for i, item in enumerate(uvreq):
        dt = datetime.strptime(item['DATE_TIME'],'%b/%d/%Y %I %p')
        if dt > now:
            uvindex = uvreq[i-1]['UV_VALUE']
            break
    if 'uvindex' not in vars():
        return  
    if uvreq:
        if uvindex <3:
            color = "\x0303"
        elif (uvindex >=3) and (uvindex < 6):
            color = "\x0308"
        elif (uvindex >=6) and (uvindex < 8):
            color = "\x0307"
        elif (uvindex >=8) and (uvindex < 11):
            color = "\x0304"
        else:
            color = "\x0306"
        max2 = max(uvreq,key=lambda uvreq: uvreq['UV_VALUE'])['UV_VALUE']
        if max2 <3:
            maxcolor = "\x0303"
        elif (max2 >=3) and (max2 < 6):
            maxcolor = "\x0308"
        elif (max2 >=6) and (max2 < 8):
            maxcolor = "\x0307"
        elif (max2 >=8) and (max2 < 11):
            maxcolor = "\x0304"
        else:
            maxcolor = "\x0306"
        return ", UV:{}{}\x0F|{}{}\x0F".format(color,uvindex,maxcolor,max2)
    else:
        return ''

def get_wind(forecast):
    try:
        if forecast.json()['flags']['units'] == 'us':
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data / 0.62137)
            m_s = float(round(wind_data, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'mph'
        elif forecast.json()['flags']['units'] == 'si':
            wind_data = forecast.json()['currently']['windSpeed']
            m_s = float(wind_data)
            kph = float(m_s * 3.6)
            speed = int(round(kph / 1.852, 0))
            unit = 'm/s'
        elif forecast.json()['flags']['units'] == 'ca':
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data)
            m_s = float(round(kph / 3.6, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'm/s'
        else:
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data / 0.62137)
            m_s = float(round(wind_data, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'mph'
        degrees = int(forecast.json()['currently']['windBearing'])
    except (KeyError, ValueError):
        return 'unknown'
    if speed < 1:
        description = 'Calm'
    elif speed < 4:
        description = 'Light air'
    elif speed < 7:
        description = 'Light breeze'
    elif speed < 11:
        description = 'Gentle breeze'
    elif speed < 16:
        description = 'Moderate breeze'
    elif speed < 22:
        description = 'Fresh breeze'
    elif speed < 28:
        description = 'Strong breeze'
    elif speed < 34:
        description = 'Near gale'
    elif speed < 41:
        description = 'Gale'
    elif speed < 48:
        description = 'Strong gale'
    elif speed < 56:
        description = 'Storm'
    elif speed < 64:
        description = 'Violent storm'
    else:
        description = 'Hurricane'
    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = u'\u2193'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = u'\u2199'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = u'\u2190'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = u'\u2196'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = u'\u2191'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = u'\u2197'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = u'\u2192'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = u'\u2198'
    return description + ' ' + str(m_s) + unit + '(' + degrees + ')'

def get_alert(forecast):
    try:
        fullalerts = []
        if forecast.json()['alerts'][0]:
            for alerts in forecast.json()['alerts']:
                title = alerts['title']
                alert = get_short_url(alerts['uri'])
                fullalerts.append("{} {}".format(title, alert))
            return ' | Alert: {}'.format(", ".join(fullalerts))
        else:
            return ''
    except:
        return ''

def get_forecast(bot,trigger,location=None):
    global forecastapi
    forecast,woeid,body,first_result,alert,result,postal,error = '','','','','','','',''
    if not location:
        woeid = bot.db.get_nick_value(trigger.nick, 'woeid')
        if not woeid:
            bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
            error = 'yes'
            return location, forecast, postal, error
        body = reversewoeid_search(woeid)
        result = body.json()['query']['results']['place']
        longlat = result['centroid']['latitude']+","+result['centroid']['longitude']
    else:
        location = location.strip()
        longlat = None
        woeid = bot.db.get_nick_value(location, 'woeid')
        if woeid is None:
            first_result = woeid_search(location)
            result = first_result.json()['query']['results']['place']
            if type(result) is list:
                woeid = 'filler'
                longlat = result[0]['centroid']['latitude']+","+result[0]['centroid']['longitude']
            else:
                woeid = 'filler'
                longlat = result['centroid']['latitude']+","+result['centroid']['longitude']
    if not woeid:
        bot.reply("I don't know where that is.")
        error = 'yes'
        return location,forecast, postal, error
    forecast = requests.get('https://api.darksky.net/forecast/{0}/{1}?units=auto'.format(forecastapi,longlat))
    if body:
        result = body.json()['query']['results']['place']
        if result['locality1']:
            location = result['locality1']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
        else:
            location = result['admin2']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
        if result['country']['content'] == 'United States':
            postal = result['postal']['content'] if result.get('postal') else None
        else:
            postal = None
    else:
        result = first_result.json()['query']['results']['place']
        if type(result) is list:
            if result[0]['locality1']:
                location = result[0]['locality1']['content'] + ", " + (result[0]['admin1']['code'].split("-")[-1] if result[0]['admin1']['code'] != '' else result[0]['country']['content'])
            elif result[0]['admin2']:
                location = result[0]['admin2']['content'] + ", " + (result[0]['admin1']['code'].split("-")[-1] if result[0]['admin1']['code'] != '' else result[0]['country']['content'])
            elif result[0]['admin1']:
                location = result[0]['admin1']['content'] + ", " + result[0]['country']['content']
            else:
                location = result[0]['name']
            if result[0]['country']['content'] == 'United States':
                postal = result[0]['postal']['content'] if result[0].get('postal') else None
            else:
                postal = None
        else:
            if result['locality1']:
                location = result['locality1']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
            elif result['admin2']:
                location = result['admin2']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
            elif result['admin1']:
                location = result['admin1']['content'] + ", " + result['country']['content']
            else:
                location = result['name']
            if result['country']['content'] == 'United States':
                postal = result['postal']['content'] if result.get('postal') else None
            else:
                postal = None
    return location, forecast, postal, error

def get_sun(tz, forecast):
    if 'sunriseTime' not in forecast:
        return ""
    sunrise = datetime.fromtimestamp(forecast['sunriseTime'], tz=timezone(tz)).strftime('%H:%M')
    sunset = datetime.fromtimestamp(forecast['sunsetTime'], tz=timezone(tz)).strftime('%H:%M')
    return ", \u2600 \u2191 " + sunrise + " \u2193 " + sunset

def get_moon(forecast):
    if 'moonPhase' not in forecast:
        return ""
    moonphase = forecast['moonPhase']
    if moonphase == 0:
        moon = "\U0001F311 | New Moon ({0:.0f}%)".format(moonphase * 100)
    elif (moonphase > 0) and (moonphase <=0.24):
        moon = "\U0001F312 | Waxing Crescent ({0:.0f}%)".format(moonphase * 100)
    elif moonphase == 0.25:
        moon = "\U0001F313 | First Quarter ({0:.0f}%)".format(moonphase * 100)
    elif (moonphase >0.25) and (moonphase <=0.49):
        moon = "\U0001F314 | Waxing Gibbous ({0:.0f}%)".format(moonphase * 100)
    elif moonphase == 0.50:
        moon = "\U0001F315 | Full Moon ({0:.0f}%)".format(moonphase * 100)
    elif (moonphase >0.50) and (moonphase <=0.74):
        moon = "\U0001F316 | Waning Gibbous ({0:.0f}%)".format(moonphase * 100)
    elif moonphase == 0.75:
        moon = "\U0001F317 | Last Quarter ({0:.0f}%)".format(moonphase * 100)
    elif (moonphase >0.75) and (moonphase <=0.99):
        moon = "\U0001F318 | Waning Crescent ({0:.0f}%)".format(moonphase * 100)
    else:
        return ""
    return ", Moon: {}".format(moon)

@commands('weather7', 'wea7', 'w7')
@example('.weather7 London')
def weather7(bot,trigger):
    location = trigger.group(2)
    if not location:
        location, forecast, postal, error = get_forecast(bot,trigger)
    else:
        location, forecast, postal, error = get_forecast(bot,trigger,location)
    if error:
        return
    summary = forecast.json()['daily']['summary']
    sevendays = []
    weekdays = {1:'M',2:'Tu',3:'W',4:'Th',5:'F',6:'Sa',7:'Su'}
    for day in forecast.json()['daily']['data']:
        wkday = weekdays[datetime.fromtimestamp(int(day['time'])).isoweekday()]
        maxtemp = round(day['temperatureMax'])
        mintemp = round(day['temperatureMin'])
        sevendays.append("{0}:({1}|{2})".format(wkday,mintemp,maxtemp))
    del sevendays[0]
    sevendays = ", ".join(sevendays)
    bot.say("{0}: [{1}] {2}".format(location, summary, str(sevendays)))

@commands('tmp', 'temp')
@example('.temp London')
def weather(bot, trigger):
    """.weather location - Show the weather at the given location."""
    location = trigger.group(2)
    if not location:
        location, forecast, postal, error = get_forecast(bot,trigger)
    else:
        location, forecast, postal, error = get_forecast(bot,trigger,location)
    if error:
        return
    summary = forecast.json()['currently']['summary']
    temp = get_temp(forecast)
    alert = get_alert(forecast)
    bot.say(u'%s: %s, %s %s' % (location, summary, temp,  alert))

@commands('wea','weather', 'wf')
def weatherfull(bot, trigger):
    """.weather location - Show the weather at the given location."""
    location = trigger.group(2)
    if not location:
        location, forecast, postal, error = get_forecast(bot,trigger)
    else:
        location, forecast, postal, error = get_forecast(bot,trigger,location)
    if error:
        return
    summary = forecast.json()['currently']['summary']
    temp = get_temp(forecast)
    humidity = forecast.json()['currently']['humidity']
    wind = get_wind(forecast)
    alert = get_alert(forecast)
    uv = get_uv(postal) if postal else ''
    sun = get_sun(forecast.json()['timezone'], forecast.json()['daily']['data'][0])
    bot.say(u'%s: %s, %s, Humidity: %s%%, %s%s%s%s' % (location, summary, temp, round(humidity*100), wind, sun, uv, alert))

@commands('moon')
def moon(bot,trigger):
    location = trigger.group(2)
    if not location:
        location, forecast, postal, error = get_forecast(bot,trigger)
    else:
        location, forecast, postal, error = get_forecast(bot,trigger,location)
    if error:
        return
    moon = get_moon(forecast.json()['daily']['data'][0])[1:]
    bot.say(moon)
    
@commands('setlocation', 'setwoeid')
@example('.setlocation Columbus, OH')
def update_woeid(bot, trigger):
    """Set your default weather location."""
    if not trigger.group(2):
        bot.reply('Give me a location, like "Washington, DC" or "London".')
        return NOLIMIT
    first_result = woeid_search(trigger.group(2))
    if first_result is None:
        return bot.reply("I don't know where that is.")
    if type(first_result.json()['query']['results']['place']) is list:
        found = first_result.json()['query']['results']['place'][0]
    else:
        found = first_result.json()['query']['results']['place']
    woeid = found['woeid']
    bot.db.set_nick_value(trigger.nick, 'woeid', woeid)
    neighborhood = found['locality2'] or ''
    if neighborhood:
        neighborhood = neighborhood['#text'] + ', '
    city = found['locality1'] or ''
    # This is to catch cases like 'Bawlf, Alberta' where the location is
    # thought to be a "LocalAdmin" rather than a "Town"
    if city:
        city = city['content']
    else:
        city = found['name']
    state = found['admin1']['content'] or ''
    country = found['country']['content'] or ''
    uzip = found['postal'] or ''
    if uzip:
        uzip = uzip['content']
    bot.reply('I now have you at WOEID %s (%s%s, %s, %s %s)' %
              (woeid, neighborhood, city, state, country, uzip))
