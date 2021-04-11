
#chat_id = "https://api.telegram.org/bot1776664489:AAGN98t5Za0lj44BCktiq-QTGAs1i4OHZ9c/getUpdates"
# token of bot
token = "1776664489:AAGN98t5Za0lj44BCktiq-QTGAs1i4OHZ9c"


#bot_id = [-598143010] #-1001347129735, ]
##my details
bot_id = [1362506121]
chat_id = [-598143010]#[1362506121]

#bot_id = [892842231]
#chat_id = [-1001178327960] #,[-1001347129735]
#-1001178327960


button_url = ["https://t.me/tbocker", "https://t.me/tbocker"]
button_text = ['order', 'service']
image = 'photo.jpg'

# duration in mint
duration = 4
text = """hi this is a sample
you can do it like this
hello there"""

import requests,os

url = 'https://api.telegram.org/bot%s/%s' % (token, 'getFile')
params={"chat_id":1362506121 , "file_id": 'AgACAgUAAxkBAAOZYFkLb8PNWyW10M8DsGDqbeujw8EAAsesMRtMzMlWJBqYFOEa4MoitxVvdAADAQADAgADeAADRicDAAEeBA'}

res = requests.get(url, params)
res = res.json()


response = requests.get('https://api.telegram.org/file/bot%s/%s' % (token, res['result']['file_path']))
dst_file_path = os.path.join(os.getcwd(), "file_name.jpg")
with open(dst_file_path, 'wb+') as f:
    f.write(response.content)