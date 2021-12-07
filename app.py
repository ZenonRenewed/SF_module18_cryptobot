import telebot
from extensions import keys, TOKEN
from utils import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help']) #обработчик команд /start, /help
def help(message: telebot.types.Message):
    text = 'Crypto Converter by Dolgopolov Gleb\n\n\
Чтобы произвести конвертацию валют введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\n \
Получить список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values']) #обработчик команды /values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ]) #обработчик сообщений с запросом на конвертацию валют
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ') #преобразование параметров из сообщения в список

        if len(values) != 3: #проверка правильного количества параметров
            raise APIException('Неверное количество параметров')

        quote, base, amount = values #передача параметров в конвертер
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e: #исключение при ошибке со стороны пользователя
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e: #исключение при ошибке со стороны программы
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else: #отправка итога конвертации
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
