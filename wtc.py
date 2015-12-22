#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Updater
from bs4 import BeautifulSoup
import requests

url = "http://whatthecommit.com/"

TOKEN=""

# Command Handlers
def start(bot, update):
    bot.polling(none_stop=True)
    bot.sendMessage(update.message.chat_id, text='Hello! I\'m the WhatTheCommit bot!')

def help(bot, update):
    text=''
    text+="/getcommit - get a random commit message!\n"
    text+="/help - show this message\n"
    bot.sendMessage(update.message.chat_id, text)

def getcommit(bot, update, args):
    # Realizamos la petición a la web
    req = requests.get(url)

    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:
        html = BeautifulSoup(req.text, "lxml")
        text = html.find_all('p')
        text = str(text[0])
        text=text[3:-5]
    else:
        print "Status Code %d" %statusCode
        text="I can't get the commit =("
        
    bot.sendMessage(update.message.chat_id, text)

def main():
    f = open('/home/ubuntu/workspace/WhatTheCommit/id/token.id', 'r')
    TOKEN=f.read()
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("getcommit", getcommit)
    dp.addTelegramCommandHandler("help", help)

    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
