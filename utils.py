import requests
from extra import token
import os


def download_image(chat_id, photo_id, index):
    url = 'https://api.telegram.org/bot%s/%s' % (token, 'getFile')
    params = {"chat_id": chat_id, "file_id": photo_id}
    res = requests.get(url, params)
    res = res.json()
    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (token, res['result']['file_path']))
    dst_file_path = os.path.join(os.getcwd(), "photo.jpg"+str(index))
    with open(dst_file_path, 'wb+') as f:
        f.write(response.content)
