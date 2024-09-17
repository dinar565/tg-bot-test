from telebot import types
from telebot.util import quick_markup


def get_root_markup():
    return build_reply_markup(["Show next training", "Add new training"])


def get_inline_markup(buttons, row_width=1):
    markup_template = {}
    for item in buttons.items():
        markup_template[item[0]] = {'callback_data': item[1]}
    return quick_markup(markup_template, row_width=row_width)


def build_reply_markup(button_names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in button_names:
        item = types.KeyboardButton(name)
        markup.add(item)
    return markup
