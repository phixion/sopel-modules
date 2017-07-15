from pushbullet import Pushbullet
import sopel

@sopel.module.commands('pushbullet','pb','alarm','push')
def pushbullet(bot, trigger):
    if trigger.nick == 'BOTOWNER_NICK' or trigger.nick == 'BOTADMIN_NICK':
        url = trigger.group(2)
        pb = Pushbullet('YOUR_API_KEY')
        pb.push_link(url,url)
