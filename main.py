from bot import MyBot
from extra import token, chat_id, bot_id
from utils import download_image
import time
import threading
import telegram
import telegram.ext


bot = MyBot(bot_token=token)

send_message = False
has_message = False
duration = 10
message = []
button_url = []
button_text = ['order', 'service']
current_command = ''
temp_but = []
buttons = []
message_sending_index = 0

#####################ui###############################################
help_button = telegram.InlineKeyboardButton(
    text='Help', # text that show to user
    callback_data='help' # text that send to bot when user tap button
    )
time_button = telegram.InlineKeyboardButton(
    text='update time', # text that show to user
    callback_data='time' # text that send to bot when user tap button
    )
send_button = telegram.InlineKeyboardButton(
    text='send message', # text that show to user
    callback_data='send' # text that send to bot when user tap button
    )
stop_button = telegram.InlineKeyboardButton(
    text='stop sending', # text that show to user
    callback_data='stop' # text that send to bot when user tap button
    )
delete_button = telegram.InlineKeyboardButton(
    text='delete Add', # text that show to user
    callback_data='del' # text that send to bot when user tap button
    )
show_button = telegram.InlineKeyboardButton(
    text='show Add', # text that show to user
    callback_data='show' # text that send to bot when user tap button
    )

add_button = telegram.InlineKeyboardButton(
    text='add Add', # text that show to user
    callback_data='add' # text that send to bot when user tap button
    )

u = None
c = None


def ui(update, context):
    global u, c
    u = update
    c = context
    bot.send_mess_with_b(
        chat_id=bot_id[0],
        text='*******menu*******',
        buttons = telegram.InlineKeyboardMarkup([[show_button, delete_button],[ time_button],[add_button], [send_button], [stop_button]])
        )


def callback_query_handler(update, context):
    cqd = update.callback_query.data
    if cqd == 'help':
        help(u, c)
    if cqd == 'add':
        add(u, c)
    if cqd == 'del':
        delete(u, c)
    if cqd == 'time':
        up_time(u, c)
    if cqd == 'stop':
        stop(u, c)
    if cqd == 'send':
        send(u, c)
    if cqd == 'show':
        show(u, c)


####################################################################################

def start_message_sending():
    global chat_id, message, message_sending_index, send_message
    while True:
        while send_message:
            if message_sending_index == 0:
                for i, mess in enumerate(message):
                    button = []
                    button.append(['order', button_url[i][0]])
                    button.append(['service', button_url[i][1]])
                    bot.send_image_with_button_caption(chat_id, mess, 'photo.jpg'+str(i), button)
                time.sleep(duration)
                print("sent...")
            else:
                button = []
                button.append(['order', button_url[message_sending_index-1][0]])
                button.append(['service', button_url[message_sending_index-1][1]])
                bot.send_image_with_button_caption(chat_id, message[message_sending_index-1], 'photo.jpg' + str(message_sending_index-1), button)
                time.sleep(duration)
                print("sent...")


def send(update, context):
    global send_message, current_command, has_message
    current_command = 'start'
    if has_message:
        reply = '***choose an message index for sending***\n'
        reply = reply + "0-> to send all message\n"
        for i, mess in enumerate(message):
            reply = reply + str(i+1) + "-> " + mess + "\n"
            current_command = 'mess_ind'
        update.message.reply_text(reply)
        #update.message.reply_text('ADD sending started with {} mint. interval'.format(duration))
    else:
        update.message.reply_text("please add an ADD first with /add..")


def help(update, context):
    global current_command
    current_command = 'help'
    message="""/start to start sending message
/stop to stop sending message
/del to delete the message
/show to show the active message
/add to add the new message
/time to add or update time    
/new 
    """
    update.message.reply_text(message)


def show(update, context):
    global message, has_message, current_command
    if has_message and len(message) != 0:
        current_command = 'show'
        for i, mess in enumerate(message):
            button = []
            button.append(['order', button_url[i][0]])
            button.append(['service', button_url[i][1]])
            bot.send_image_with_button_caption(chat_id, mess, 'photo.jpg' + str(i), button)
    else:
        update.message.reply_text("no add to show add first with /add..")


def up_time(update, context):
    global current_command
    current_command = 'time'
    update.message.reply_text("current duration is {}. Set a new duration by /time".format(duration))


def delete(update, context):
    global send_message, message, button_url, current_command ,has_message
    if len(message) == 0:
        update.message.reply_text('no message to del')
        return
    current_command = 'delete'
    reply = '***choose an index for delete***\n'
    for i, mess in enumerate(message):
        reply = reply + str(i)+"-> " + mess + "\n"
        current_command = 'del_ind'
    update.message.reply_text(reply)


def stop(update, context):
    global send_message, current_command
    if send_message:
        current_command = 'stop'
        send_message = False
        update.message.reply_text('ADD sending stopped..')
        return
    update.message.reply_text('you are not sending any message..')


def add(update, context):
    global send_message, current_command
    current_command = 'message'
    send_message = False
    update.message.reply_text('please enter text for ADD..')


def echo_text(update, context):
    global current_command, duration, message, button_url, has_message, temp_but,\
        buttons, send_message, message_sending_index
    if current_command == 'time':
        try:
            duration = int(update.message.text)
            update.message.reply_text("duration updated to "+ update.message.text)
        except:
            update.message.reply_text("please enter a number..")

    if current_command == 'message':
        message.append(update.message.text)
        current_command = 'upload'
        update.message.reply_text("Upload photo for Add..")

    if current_command == 'o' or current_command == 's':
        if current_command == 'o':
            temp_but = []
            temp_but.append(update.message.text)
            update.message.reply_text("Enter link for service button")
            current_command = 's'

        else:
            current_command = 'done'
            temp_but.append(update.message.text)
            button_url.append(temp_but)
            print("but", button_url)

            update.message.reply_text("add added..")
            #bot.send_image_with_button_caption(bot_id, message[0], 'photo.jpg', buttons)
            #update.message.reply_text("Set a duration by /time..current duration is {}".format(duration))
            has_message = True

    if current_command == 'del_ind':
        # delete mess button photo button url
        index = int(update.message.text)
        del message[index]
        del button_url[index]
        if len(message) == 0:
            has_message = False

        update.message.reply_text('ADD deleted..add a new one with /add')
        current_command = ''

    if current_command == 'mess_ind':
        message_sending_index = int(update.message.text)
        send_message = True
        current_command = ''


def echo_photo(update, context):
    global message
    global current_command
    if current_command == 'upload':
        current_command = 'o'
        chat = update.message['chat']['id']
        photo_id = update.message['photo'][0]['file_id']
        download_image(chat, photo_id, len(message)-1)
        update.message.reply_text("enter link for order button..")


bot.add_command_handler('start', ui)
bot.add_query_handler(callback_query_handler)

bot.add_command_handler('send', send)
bot.add_command_handler('help', help)
bot.add_command_handler('show', show)
bot.add_command_handler('del', delete)
bot.add_command_handler('stop', stop)
bot.add_command_handler('time', up_time)
bot.add_command_handler('add', add)
bot.add_message_handler_text(echo_text)
bot.add_message_handler_photo(echo_photo)

mess = threading.Thread(target=start_message_sending)
mess.start()
bot.start_polling()



