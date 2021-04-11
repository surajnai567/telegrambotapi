import requests
#from config import token
import schedule
import os
from bot import MyBot

token = os.getenv('my_token')
def download_image(chat_id, photo_id, index):
    url = 'https://api.telegram.org/bot%s/%s' % (token, 'getFile')
    params = {"chat_id": chat_id, "file_id": photo_id}
    res = requests.get(url, params)
    res = res.json()
    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (token, res['result']['file_path']))
    dst_file_path = os.path.join(os.getcwd(), "photo.jpg"+str(index))
    with open(dst_file_path, 'wb+') as f:
        f.write(response.content)


def send_message(mess, order, service, image, chat_id, bot):
    button = []
    button.append(['order', order])
    button.append(['service', service])
    bot.send_image_with_button_caption(chat_id, mess, 'photo.jpg'+str(image), button)


def sending_job(bot, message, button, image_index, chat_id):
    bot.send_image_with_button_caption(chat_id, message, 'photo.jpg' + str(image_index), button)


def sc_job(func, *args, **kwargs):
    schedule.every(1).minute().do(func, args, kwargs)


def download_video(chat_id, file_id, filename):
    url = 'https://api.telegram.org/bot%s/%s' % (token, 'getFile')
    params = {"chat_id": chat_id, "file_id": file_id}
    res = requests.get(url, params)
    res = res.json()
    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (token, res['result']['file_path']))
    dst_file_path = os.path.join(os.getcwd(), filename)
    with open(dst_file_path, 'wb+') as f:
        f.write(response.content)


def delete_video_photo(filename):
    os.remove(os.path.join(os.getcwd(), filename))


def job_sending(bot:MyBot, chat_id:list, message:str, button:list, image_name:str):
    mess = message
    butt = button.copy()
    chat = chat_id.copy()
    url = image_name
    video_extension = ['avi', 'mp4', 'mkv', '3gp']
    if url.split(".")[-1].lower() in video_extension:
        bot.send_video_with_button_caption(chat, mess, url, butt)
    else:
        bot.send_image_with_button_caption(chat, mess, url, butt)

