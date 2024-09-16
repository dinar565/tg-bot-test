import os
import random
import telebot

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Test welcome',
                     parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, 'Just text')

if __name__ == '__main__':
    bot.infinity_polling()
