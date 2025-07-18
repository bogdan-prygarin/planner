import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = '8095977538:AAG12roxi2PzhQl8v3jvZI9x4V3qCdtMMZo'

# 🌐 Ссылка на веб-приложение
WEB_APP_URL = 'https://d92ed8afb0f7a5.lhr.life'  # замени на свою ссылку

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Мои планы", web_app=WebAppInfo(url=WEB_APP_URL))
    btn2 = InlineKeyboardButton("+ Новое событие", callback_data="new_task")
    btn3 = InlineKeyboardButton("Удалить событие", callback_data="delete_task")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "Привет! Тут ты можешь планировать события.",
        reply_markup=markup
    )


@bot.callback_query_handler()
def callback_query_handler(callback):
    markup = InlineKeyboardMarkup()
    callbackData = callback.data

    if callbackData == "new_task":
        btn1 = InlineKeyboardButton("Мини приложение", web_app=WebAppInfo(url=WEB_APP_URL))
        markup.add(btn1)
        bot.send_message(
            callback.message.chat.id,
            'Чтоб добавить новое событие, напишите в сообщение в таком формате: \n\n```событие&время&дата Ваш текст события & --:-- & --.--.--``` \n\n*Для удобства использования, рекомендуем пользоватся мини приложением!*',
            parse_mode="markdown",
            reply_markup=markup
        )

    if callbackData == "delete_task":
        btn1 = InlineKeyboardButton("Мини приложение", web_app=WebAppInfo(url=WEB_APP_URL))
        markup.add(btn1)
        bot.send_message(
            callback.message.chat.id,
            '*Чтоб удалить событие, необходимо воспользоватся мини приложением!*',
            parse_mode="markdown",
            reply_markup=markup
        )

bot.polling()
