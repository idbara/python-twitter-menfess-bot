import tweepy
import config
from datetime import datetime
import pytz
import sys
from time import sleep

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


def debug_cuy(text):
    print(pytz.timezone("Asia/Jakarta").localize(datetime.now()).strftime("%H:%M:%S") + ' => ' + str(text))


def delete_message(message_id):
    debug_cuy("👋 menghapus pesan dengan id " + str(message_id))
    api.destroy_direct_message(message_id)


def make_tweet(text):
    try:
        debug_cuy("🚀 membuat tweet baru")
        api.update_status(text)
    except tweepy.TweepError as e:
        debug_cuy('😡 ' + e.response.json()['errors'][0]['message'].lower())
        pass


while True:
    # * mencoba mengambil pesan
    try:
        list = api.list_direct_messages()
        list.reverse()  # * mengurutkan dari yang terlama
        # * cek isi list tidak 0
        if len(list) is not 0:
            for x in range(len(list)):
                message_id = list[x].id
                message_data = list[x].message_create['message_data']
                message_data_text = message_data['text']
                debug_cuy('💌 ada pesan "'+message_data_text+'"')
                # * cek ada keyword
                if "[ask]" or "[Ask]" or "[ASK]" in message_data_text and len(message_data_text) <= 280:
                    debug_cuy('👍 kriteria pesan sesuai')
                    # * mencoba cek ada attachment tidak
                    try:
                        message_data_attachment_media_type = message_data['attachment']['media']['type']
                        if message_data_attachment_media_type == 'photo':
                            debug_cuy('😓 belom support photo')
                            delete_message(message_id)
                        else:
                            debug_cuy('😓 belom support video')
                            delete_message(message_id)
                    # * handle jika cuma text
                    except:
                        # * membuat tweet
                        make_tweet(message_data_text)
                        delete_message(message_id)
                else:
                    debug_cuy('👎 pesan tidak sesuai kriteria')
                    delete_message(message_id)
        # * handle jika isi list kosong
        else:
            debug_cuy('⏳ isi pesan kosong, menunggu pesan baru, cek setiap 1 menit, sisa limit ' + str(api.rate_limit_status()['resources']['direct_messages']['/direct_messages/events/list']['remaining']))
        # sleep(60)
    # ! handle jika ada error
    except tweepy.RateLimitError as e:
        debug_cuy('😡 ' + e.response.json()['errors'][0]['message'].lower())
        sleep(60)
        pass
    except tweepy.TweepError as e:
        debug_cuy('😡 ' + e.response.json()['errors'][0]['message'].lower())
        pass
