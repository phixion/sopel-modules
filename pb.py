from pushbullet import Pushbullet
import sopel

@sopel.module.commands('pushbullet','pb','alarm','push')
def pushbullet(bot, trigger):
    if trigger.nick == 'Phixion' or trigger.nick == 'vespertine':
        url = trigger.group(2)
        pb = Pushbullet('YOUR_API_KEY)
        pb.push_link(url,url)
