# coding=utf-8
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random as r
import requests
import telebot
from tokenName import tokenId

token = tokenId
telegramPath = "https://api.telegram.org/bot"
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def hello(message):
    bot.reply_to(message,"Send the number of colors.")

@bot.message_handler(func = lambda mess: True)
def prof(message):
    messageContent = message.text
    messageChatId = message.chat.id
    if messageContent in ['1', '2', '3', '4', '5']:
        generator(messageContent)
        sendPhoto(messageChatId)
    else:
        responseMessage = "I need a number between 1 and 5.\nPlease try again with another number."
        sendMessage(messageChatId, responseMessage)
    return

def sendPhoto(messageChatId):
    urlPath = telegramPath + token + "/sendPhoto";
    photoFile = {'photo': open('./img.png', 'rb')}
    userChatId = {'chat_id' : messageChatId}
    request = requests.post(urlPath, files = photoFile, data = userChatId)
    return

def sendMessage(messageChatId, responseMessage):
    urlPath = telegramPath + token + '/sendMessage'
    data = {'chat_id': messageChatId, 'text': responseMessage}
    request = requests.post(urlPath, data=data)
    return

def generator(imput):
    numberOfColors = int(imput)
    url = 'http://palett.es/API/v1/palette'
    if numberOfColors>5:
        return generator(5)
    elif numberOfColors<1:
        return generator(1)
    else:
        json_request = requests.get(url).json()
        colors = [color.upper() for color in json_request]
        fractions = [20]*5
        positions = [0,1,2,3,4]
        for i in range(5-numberOfColors):
            chosenColor = r.choice(positions)
            positions.remove(chosenColor)
            fractions[chosenColor] = 0
        fig, ax = plt.subplots(figsize=(4.8, 4.8))
        pie = plt.pie(fractions, colors = colors, startangle=27.11)
        fig.set_facecolor("black")
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.margins(0, 0)
        ax.axis('equal')    
        image = plt.savefig('img', dpi=500)
        plt.close()

bot.polling()
