import os
import traceback

import telebot
import training_service as ts
import markup_service as ms
from telebot import types

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id, 'Welcome to Lorenzo Training Helper!',
                     reply_markup=ms.get_root_markup())


@bot.message_handler(commands=['new_training'])
def add_new_training(message: types.Message):
    ts.add_new_training(message)
    bot.send_message(message.chat.id,
                     'Please follow ',
                     parse_mode='markdown')


@bot.message_handler(commands=['show_next_training'])
def show_next_training(message: types.Message):
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, your next training is: {ts.get_next_training()}',
                     parse_mode='markdown',
                     reply_markup=ms.get_inline_markup({"Complete training": "complete_training"}))


@bot.message_handler(func=lambda message: True)
def echo(message: types.Message):
    if message.text == "Show next training":
        show_next_training(message)
    elif message.text == "Add new training":
        add_new_training(message)
    else:
        bot.send_message(message.chat.id, 'Just text', reply_markup=ms.get_root_markup())


@bot.callback_query_handler(func=lambda callback: callback.data == "complete_training")
def complete_training(callback: types.CallbackQuery):
    try:
        ts.complete_training(callback.message)
        bot.send_message(callback.message.chat.id,
                         f"{callback.from_user.first_name}, congratulations for training completion!",
                         parse_mode='markdown',
                         reply_markup=ms.get_root_markup())
    except Exception as e:
        traceback.print_exc()
        raise


if __name__ == '__main__':
    bot.infinity_polling()
