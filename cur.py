import requests
import sys
import json
import sopel

last_prices = {}
main_coins = ["btc", "xrp", "eth"]
single_url = "http://api.cryptocoincharts.info/tradingPair/{0}_{1}"
multi_url = "http://api.cryptocoincharts.info/tradingPairs"

@sopel.module.rule('^\.(\w+)2(\w+)\s?(.+)?$')
def crypto_exchange(bot, trigger):
  from_cur = trigger.group(1)
  to_cur = trigger.group(2)
  quantity = float(trigger.group(3)) if trigger.group(3) is not None else 1

  api_result = requests.get(single_url.format(from_cur, to_cur)).json()
  calc_result = quantity * float(api_result["price"])

  bot.say("{0} {1} is about {2:.4f} {3}".format(quantity, api_result["coin1"], float(calc_result), api_result["coin2"]))

@sopel.module.rule('^\.({0})$'.format("|".join(main_coins)))
def crypto_spot(bot, trigger):
  from_cur = trigger.group(1)
  global last_prices
  from_cur = from_cur.lower()
  if from_cur not in main_coins:
    bot.say("Invalid currency!")

  api_result = requests.get(single_url.format(from_cur, "usd")).json()

  if from_cur not in last_prices:
    last_prices[from_cur] = 0

  diffStr = getDiffString(float(api_result["price"]), last_prices[from_cur])
  last_prices[from_cur] = float(api_result["price"])
  bot.say("{0}: ${1:.4f}{2}".format(api_result["id"], float(api_result["price"]), diffStr))

@sopel.module.commands('ticker','tick')
def tick(bot, trigger):
  global last_prices
  pairs = ",".join(["{0}_usd".format(x) for x in main_coins])
  api_result = requests.post(multi_url, data={"pairs": pairs}).json()

  for currency in api_result:
    coin = currency["id"].split("/")[0]

    if coin not in last_prices:
      last_prices[coin] = 0

    diffStr = getDiffString(float(currency["price"]), last_prices[coin])
    last_prices[coin] = float(currency["price"])
    bot.say("{0}: ${1:.4f}{2}".format(currency["id"], float(currency["price"]), diffStr))

def getDiffString(current_price, last_price):
  diff = current_price - last_price
  diffStr = ""
  if diff != 0:
    sign = "+" if diff > 0 else ''
    diffStr = " ({0}{1:.4f})".format(sign, diff)
  return diffStr