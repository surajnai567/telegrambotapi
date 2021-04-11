import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters


class MyBot:
    def __init__(self, bot_token):
        self.token = bot_token
        self.bot = telegram.Bot(token=self.token)
        self.updater = Updater(self.token, use_context=True)
        self.dp = self.updater.dispatcher

    def set_api(self, new_token):
        self.token = new_token

    def send_message(self, text, chat_id):
        self.bot.send_message(text=text, chat_id=chat_id)

    def send_mess_with_b(self, text, chat_id, buttons):
        self.bot.send_message(text=text,chat_id=chat_id, reply_markup=buttons)


    def send_image_with_button_caption(self, chat_id, caption:str=None, image_url=None, buttons:list=[]):
        buttons = [telegram.InlineKeyboardButton(text=text, url=url) for text, url in buttons]
        markup = telegram.InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
        for chat in chat_id:
            self.bot.send_photo(chat_id=chat, photo=open(image_url, 'rb'),
                                caption=caption, reply_markup=markup)
        print("message sent....")

    def send_video_with_button_caption(self, chat_id, caption:str=None, image_url=None, buttons:list=[]):
        buttons = [telegram.InlineKeyboardButton(text=text, url=url) for text, url in buttons]
        markup = telegram.InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
        for chat in chat_id:
            self.bot.send_video(chat_id=chat, video=open(image_url, 'rb'),
                                caption=caption, reply_markup=markup)
        print("message sent....")

    def add_command_handler(self, command:str, func):
        self.dp.add_handler(CommandHandler(command, func))

    def add_message_handler_text(self, func):
        self.dp.add_handler(MessageHandler(Filters.text, func))

    def add_message_handler_video(self, func):
        self.dp.add_handler(MessageHandler(Filters.video, func))

    def add_message_handler_photo(self, func):
        self.dp.add_handler(MessageHandler(Filters.photo, func))

    def add_query_handler(self, func):
        self.dp.add_handler(telegram.ext.CallbackQueryHandler(func))

    def start_polling(self):
        self.updater.start_polling()

