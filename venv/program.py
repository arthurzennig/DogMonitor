from telegram.ext import Updater
from telegram.ext import CommandHandler
import AudioData
import telegram
from typing import Optional

TOKEN="510807200:AAHVziX8F-67Cx0pNlUc-Ph_6u6kvTOUJOA"


class TelegramDog:
    audio_filename = ""
    chat_id_collected = None
    def __init__(self):
        self.updater = Updater(token=TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.scheduled = self.updater.job_queue
        self.subscribe()

    def start(self,bot,update):
        self.chat_id_collected = update.message.chat_id
        bot.send_message(chat_id=update.message.chat_id, text="I am a bot, please talk to me")
        bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


    def dog_bark(self,bot,update):
        self.chat_id_collected = update.message.chat_id
        bot.send_message(chat_id=update.message.chat_id, text = "woof,woof,woof,woof....")

    def callback_30(self,bot,job):
        bot.send_message(chat_id=self.chat_id_collected, text = "dog dog sending message every 30 seconds...")

    def callback_now(self,bot,job):
        bot.send_message(chat_id=self.chat_id_collected, text = "A sound was detected.")
        print ("sending file:",self.audio_filename)
        bot.send_audio(chat_id=self.chat_id_collected, audio=open(self.audio_filename,'rb'))

    def greetings(self,bot,job):
        bot.send_message(chat_id=self.chat_id_collected, text = "A sound was detected.")
        print ("sending file:",self.audio_filename)
        bot.send_audio(chat_id=self.chat_id_collected, audio=open(self.audio_filename,'rb'))

    def subscribe(self):
        start_handler = CommandHandler('start', self.start)
        update_handler = CommandHandler('woof', self.dog_bark)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(update_handler)


def main():
    #instantiate object that connects to Telegram bot.
    td = TelegramDog()


    #pooling: standby for client commands. (keep ears open).
    td.updater.start_polling()
    #Watching home. Flag when listened something.
    aud = AudioData.AudioData(2200)
    while True:
        file = aud.listen()
        if file != None and td.chat_id_collected != None:
            td.audio_filename = file
            job_now = td.scheduled.run_once(td.callback_now,0)
            file = ""

    td.updater.idle()


if __name__ == "__main__":

    main()