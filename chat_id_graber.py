"""how to use
create bot from bot father and find token
add bot tot the groups or channels
send message to those groups
call this function
"""
import config
import requests
import os
#token = config.token
token = os.getenv('my_token')


def chat_id_grabber(token):
    chat_id = {}
    url = "https://api.telegram.org/bot{}/getUpdates".format(token)
    res = requests.get(url=url)
    key = res.json()
    for k in key['result']:
        print(k)
        for j in k:
            if j == "channel_post" or j == "my_chat_member":
                chat_id[k[j]['chat']['title']] = k[j]['chat']['id']
    return chat_id


if __name__ == '__main__':
    print(chat_id_grabber(config.token))