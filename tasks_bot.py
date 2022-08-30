import random
import json
from asyncio import tasks

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

TOKEN = '5749861245:AAHOOLyngTDLFdxpDHJeMEyuF2HOTTfIJ5c'


def get_task(task_name):
    mas = data['tasks'][task_name]
    return mas


def get_data():
    global data
    with open('data/tests.json') as f:
        file_content = f.read()
        data = json.loads(file_content)
    return data


def start(update, context):
    tasks = sorted(list(data['tasks_info']))
    mas = []
    now = []
    for e in tasks:
        now.append(e)
        if len(now) == 2:
            mas.append(now)
            now = []
    if now:
        mas.append(now)

    markup = ReplyKeyboardMarkup(mas, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Привет! Я провожу тесты по заданиям ЕГЭ")
    update.message.reply_text("Выбери задание", reply_markup=markup)
    return 1


def begin(update, context):
    res = update.message.text
    if res.lower() in list(data['tasks_info']):
        task = data['tasks_info'][res.lower()]
        context.user_data["right"] = 0
        context.user_data["count"] = 0
        context.user_data["mistakes"] = []
        mas = get_task(task['name'])
        context.user_data["ques"] = random.sample(mas, len(mas))
        markup = ReplyKeyboardMarkup([['/stop']], one_time_keyboard=False, resize_keyboard=True)
        qs = ' '.join([context.user_data["ques"][0]['question'], context.user_data["ques"][0]['comment']])
        update.message.reply_text(f"Отлично! {task['instruction']}", reply_markup=markup)
        update.message.reply_text("Чтобы завершить тест дай команду /stop \n Вот тебе первое слово:")
        update.message.reply_text(qs)
        return 2
    else:
        markup = ReplyKeyboardMarkup([list(data['tasks_info'])], one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text("Я не понял твой ответ... Выбери задание", reply_markup=markup)
        return 1


def ques(update, context):
    res = update.message.text
    if res == context.user_data["ques"][0]['response']:
        context.user_data["right"] += 1
        context.user_data["count"] += 1
        update.message.reply_text('+')
    else:
        res = ' '.join([context.user_data["ques"][0]['response'], context.user_data["ques"][0]['comment']])
        context.user_data["count"] += 1
        context.user_data["mistakes"].append(res)
        update.message.reply_text(f'Ошибка! Правильный ответ - {res}')
    del context.user_data["ques"][0]

    if not context.user_data["ques"]:
        return stop(update, context)
    qs = ' '.join([context.user_data["ques"][0]['question'], context.user_data["ques"][0]['comment']])
    update.message.reply_text('\n' + qs)
    return 2


def stop(update, context):
    if not context.user_data["count"]:
        update.message.reply_text(f'Тестирование завершено.', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text(f'Тестирование завершено. Балл {context.user_data["right"]} '
                                  f' из {context.user_data["count"]}', reply_markup=ReplyKeyboardRemove())
        if context.user_data["mistakes"]:
            update.message.reply_text(f'Слова, в которых вы ошиблись:\n' + '\n'.join(context.user_data["mistakes"]))
        else:
            update.message.reply_text('Молодец, все идеально!')
    update.message.reply_text('Чтобы пройти тестирование заново, дайте команду /start')
    return ConversationHandler.END


def main():
    get_data()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={
            2: [CommandHandler('stop', stop),
                MessageHandler(Filters.text, ques, pass_user_data=True)],
            1: [CommandHandler('stop', stop),
                MessageHandler(Filters.text, begin, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
