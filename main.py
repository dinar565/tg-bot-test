import os
import traceback

import telebot
import training_service as ts
import markup_service as ms
import constants as const
from telebot import types

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id, const.WELCOME_MESSAGE.format(message.from_user.first_name),
                     reply_markup=ms.get_root_markup())


@bot.message_handler(commands=['new_training'])
def add_new_training(message: types.Message):
    try:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.send_message(message.chat.id,
                         const.NEW_TRAINING_START_MESSAGE.format(message.from_user.first_name),
                         parse_mode='markdown')
        bot.register_next_step_handler(message, process_new_training)
    except Exception as e:
        traceback.print_exc()
        raise


def process_new_training(message: types.Message):
    ts.add_new_training(message)
    bot.send_message(message.chat.id,
                     const.NEW_TRAINING_ADDED_MESSAGE.format(message.from_user.first_name),
                     parse_mode='markdown')


@bot.message_handler(commands=['show_next_training'])
def show_next_training(message: types.Message):
    try:
        has_next_training, next_training = ts.get_next_training(message.from_user.first_name)
        bot.send_message(message.chat.id,
                         f'{next_training}',
                         parse_mode='markdown',
                         reply_markup=ms.get_inline_markup({"Complete training": "complete_training"})
                                      if has_next_training else ms.get_root_markup())
    except Exception as e:
        traceback.print_exc()
        raise


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
                         const.TRAINING_COMPLETED_MESSAGE.format(callback.from_user.first_name),
                         parse_mode='markdown',
                         reply_markup=ms.get_root_markup())
    except Exception as e:
        traceback.print_exc()
        raise


if __name__ == '__main__':
    bot.infinity_polling()
