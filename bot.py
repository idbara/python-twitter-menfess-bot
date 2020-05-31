import tweepy
import config
from datetime import datetime
import pytz
import sys

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


def debugCuy(text):
  print(pytz.timezone("Asia/Jakarta").localize(datetime.now()).strftime("%H:%M:%S") + ' => ' + text)


list = api.list_direct_messages()
list.reverse()
for x in range(len(list)):
  message_id = list[x].id
  message_data = list[x].message_create['message_data']
  try:
    # * ada attachment
    message_data_attachment_media_type = message_data['attachment']['media']['type']
    if message_data_attachment_media_type == 'photo':
      print('ini photo')
    elif message_data_attachment_media_type == 'video':
      print('ini video')
    else:
      pass
  except:
    # * tidak ada attachment
    message_data_text = message_data['text']
    print('ini text')
