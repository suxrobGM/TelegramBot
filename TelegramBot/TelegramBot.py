# Импорт модулей
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json, logging

# Логируем история сообщение в отдельном файле
def log_messages(bot_message, update):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Открываем файл логов для записи.
    fh = logging.FileHandler("history.log")
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    user_chat_id = update.message.chat_id
    user_message = update.message.text
    logger.info("%(username)s send message: %(message)s" %{"username":user_chat_id, "message":user_message})
    logger.info("Bot send message: %s" %bot_message)



# Настройки
TELEGRAM_BOT_TOKEN = "591333535:AAEt8h50_WfSVNh7sV9fOOibdJm2IaIXgc0"
DIALOGFLOW_CLIENT_ACCESS_TOKEN = "36e03032be3e40a7adbc94140a95b14d"
updater = Updater(token = TELEGRAM_BOT_TOKEN) # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команды
def startCommand(bot, update): #/start
    bot.send_message(chat_id=update.message.chat_id, text="Привет, давай пообщаемся?")

def scheduleCommand(bot, update): #/schedule
    bot.send_photo(chat_id=update.message.chat_id, photo="https://yadi.sk/i/Qu4uWh-E3Up9Ju") #Ссылка из Яндекс диска

def textMessage(bot, update):
    request = apiai.ApiAI(client_access_token=DIALOGFLOW_CLIENT_ACCESS_TOKEN).text_request()  #Токен API к Dialogflow
    request.lang = "ru" # На каком языке будет послан запрос
    request.session_id = "Jack_Vorobey_Bot" # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode("utf-8"))
    response = responseJson["result"]["fulfillment"]["speech"] # Разбираем JSON и вытаскиваем ответ
    
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Я Вас не совсем понял!")
    
    log_messages(bot_message=response, update=update)



# Хендлеры
start_command_handler = CommandHandler("start", startCommand)
schedule_command_handler = CommandHandler("schedule", scheduleCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(schedule_command_handler)
dispatcher.add_handler(text_message_handler)


# Начинаем поиск обновлений
updater.start_polling(clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()