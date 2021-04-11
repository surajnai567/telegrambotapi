from bot import MyBot
from extra import bot_id, chat_id
from utils import download_image, download_video, delete_video_photo, job_sending
import threading
import telegram
import telegram.ext
import time
import os
from scheduler import sch

token = os.getenv('my_token')
bot = MyBot(bot_token=token)
#sch = BlockingScheduler()
send_message = True
has_message = False
video_extension = ['avi', 'mp4', 'mkv', '3gp']
duration = 10
message = []
button_url = []
button_text = ['order', 'service']
current_command = ''
temp_but = []
buttons = []
message_sending_index = 0
list_of_active_jobs = []
list_of_time = []
attatchents = []
job_ids = []
temp = []
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
    text='resend stop messages', # text that show to user
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
    pass
#    sch.start()
    #while True:
     #   while send_message:
            #schedule.run_pending()

            #if message_sending_index == 0:
                #for i, mess in enumerate(message):
                #    button = []
                #    button.append(['order', button_url[i][0]])
                #    button.append(['service', button_url[i][1]])
                #    bot.send_image_with_button_caption(chat_id, mess, 'photo.jpg'+str(i), button)
                #time.sleep(duration)
                #print("sent...")
            #else:
               # button = []
                #button.append(['order', button_url[message_sending_index-1][0]])
                #button.append(['service', button_url[message_sending_index-1][1]])
                #bot.send_image_with_button_caption(chat_id, message[message_sending_index-1], 'photo.jpg' + str(message_sending_index-1), button)
               # time.sleep(duration)
                #print("sent...")


def send(update, context):
    global send_message, current_command, has_message
    current_command = 'start'
    if has_message:
        reply = '***choose an message index for start sending***\n'
        for i, mess in enumerate(message):
            reply = reply + str(i) + "-> " + mess + "\n"
            current_command = 'restart_index'
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
            if attatchents[i].split('.')[-1].lower() in video_extension:
                #send video message
                bot.send_video_with_button_caption(bot_id, mess, image_url=attatchents[i], buttons=button)
            else:
                bot.send_image_with_button_caption(bot_id, mess, attatchents[i], button)
    else:
        update.message.reply_text("no add to show add first with /add..")


def up_time(update, context):
    global current_command
    if not has_message:
        update.message.reply_text('no add is available')
        return
    current_command = 'time_index'
    reply = '***choose an message index for updating time***\n'
    for i, mess in enumerate(message):
        reply = reply + str(i) + "-> " + mess + "\n"
        #current_command = 'mess_ind'
    update.message.reply_text(reply)
    #update.message.reply_text("current duration is {}. Set a new duration by /time".format(duration))


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
    #if send_message:
    #    current_command = 'stop'
     #   send_message = False
      #  update.message.reply_text('ADD sending stopped..')
       # return
    if has_message:
        current_command = 'stop'
        reply = '***choose an index for stopping***\n'
        for i, mess in enumerate(message):
            reply = reply + str(i) + "-> " + mess + "\n"
            current_command = 'stop_index'
        update.message.reply_text(reply)
        return
    update.message.reply_text('you are not sending any message..')


def add(update, context):
    global send_message, current_command, temp
    temp = []
    current_command = 'message'
    send_message = False
    update.message.reply_text('please enter text for ADD..')


def echo_text(update, context):
    global current_command, duration, message, button_url, has_message, temp_but,\
        buttons, send_message, mssage_sending_index, time_index, list_of_time, temp

    if current_command == 'stop_index':
        index = int(update.message.text)
        #sch.pause_job(index)
        list_of_active_jobs[index].pause()
        update.message.reply_text(message[index] + " is stopped..")

    if current_command == 'restart_index':
        index = int(update.message.text)
        #sch.resume_job(index)
        list_of_active_jobs[index].resume()
        update.message.reply_text(message[index] + " is restarted..")

    if current_command == 'message_time':
        current_command = 'done'
        #list_of_time.append(int(update.message.text))
        temp.append(int(update.message.text))
        update.message.reply_text("added to list of add..")
        # use temp to append data into table
        print(temp)
        message.append(temp[0])
        attatchents.append(temp[1])
        button_url.append(temp[2])
        list_of_time.append(temp[3])
        temp = []
        print(temp)

        if len(message):
            index = len(message) - 1
            # append job here
            button = []
            button.append(['order', button_url[index][0]])
            button.append(['service', button_url[index][1]])
            #jb = lambda: job_sending(bot, chat_id, message[index], button, attatchents[index])
            list_of_active_jobs.append(sch.add_job(job_sending, args=[bot,chat_id, message[index], button, attatchents[index]] ,trigger='interval', seconds=list_of_time[index]))

    if current_command == 'time':
        try:
            #list_of_time.append(int(update.message.text))
            list_of_time[time_index] = int(update.message.text)
            #sch.reschedule_job(str(time_index), trigger='interval', seconds=int(update.message.text))
            list_of_active_jobs[time_index].reschedule(trigger ='interval', seconds=int(update.message.text))
            update.message.reply_text("duration updated to " + update.message.text)
            current_command = 'done'
        except:
            update.message.reply_text("please enter a number..")

    if current_command == 'time_index':
        current_command = 'time'
        time_index = int(update.message.text)
        update.message.reply_text("please enter a duration..")

    if current_command == 'message':
        #message.append(update.message.text)
        temp.append(update.message.text)
        current_command = 'upload'
        update.message.reply_text("Upload photo/video for Add..")

    if current_command == 'o' or current_command == 's':
        if current_command == 'o':
            temp_but = []

            temp_but.append(update.message.text)
            update.message.reply_text("Enter link for service button")
            current_command = 's'

        else:
            current_command = 'message_time'
            temp_but.append(update.message.text)
            #button_url.append(temp_but)
            temp.append(temp_but)
            time_index = len(message) - 1
            update.message.reply_text("enter message sending time gap")
            #bot.send_image_with_button_caption(bot_id, message[0], 'photo.jpg', buttons)
            #update.message.reply_text("Set a duration by /time..current duration is {}".format(duration))
            has_message = True

    if current_command == 'del_ind':
        # delete mess button photo button url
        index = int(update.message.text)
        list_of_active_jobs[index].pause()
        del button_url[index]
        delete_video_photo(attatchents[index])
        del attatchents[index]
        del message[index]
        del list_of_time[index]
        list_of_active_jobs[index].remove()
        del list_of_active_jobs[index]
        print(list_of_active_jobs, message, attatchents, list_of_time, button_url)

        if len(message) == 0:
            print("no msg")
            has_message = False

        update.message.reply_text('ADD deleted..')
        current_command = ''

    if current_command == 'mess_ind':
        message_sending_index = int(update.message.text)
        send_message =  False
        current_command = ''


def echo_photo(update, context):
    global message
    global current_command
    if current_command == 'upload':
        current_command = 'o'
        chat = update.message['chat']['id']
        photo_id = update.message['photo'][-1]['file_id']
        random_string = str(time.time())
        download_image(chat, photo_id, random_string)
        #attatchents.append('photo.jpg'+ random_string)
        temp.append('photo.jpg'+ random_string)
        update.message.reply_text("enter link for order button..")


def echo_video(update, context):
    #print(update.message['video']['file_name'],update.message['video']['file_id'])
    global message
    global current_command
    if current_command == 'upload':
        current_command = 'o'
        chat = update.message['chat']['id']
        video_id = update.message['video']['file_id']
        filename = update.message['video']['file_name']
        download_video(chat, video_id, filename)
        #attatchents.append(filename)
        temp.append(filename)
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
bot.add_message_handler_video(echo_video)
#message_sending_thread = threading.Thread(target=start_message_sending)
#message_sending_thread.start()
bot.start_polling()



