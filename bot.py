import telebot
import main 

bot = telebot.TeleBot('1873764229:AAFeZ8TubZihEe8__-IhEL2k9E2XAMCiPI4')
tovary = main.Tovary()

@bot.message_handler(commands = ['categories'])
def send_categories(message):
    params = message.text[12:]
    if len(params) >= 1:
        msgtexts = main.return_by_category(params)
        for msgtext in msgtexts:
            bot.reply_to(message, msgtext)
    else:
        msgtext = main.get_categories()
        bot.reply_to(message, msgtext)

@bot.message_handler(commands = ['product'])
def send(message):
    params = message.text[9:]
    print(params)
    if len(params) >= 1:
        msgtext = tovary.search_for_product(params)
        bot.reply_to(message, msgtext)
    else:
        msgtext = "/product {Название товара}"
        bot.reply_to(message, msgtext)


bot.polling()