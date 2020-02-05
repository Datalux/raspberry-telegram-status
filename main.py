# -*- coding: utf-8 -*-
import telegram
from telegram.ext import Updater, CommandHandler
import json
import os, subprocess
from subprocess import call

with open("config.json") as jsn:
	config = json.load(jsn)

TOKEN = config['token']
ADMIN = config['admin']

def status(bot, update):
	chat_id = update.message.chat_id
	if chat_id == ADMIN:
		t = float(subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell = True)[:-1])
		result = subprocess.check_output("df -h .", shell = True)
		output = result.split()
		disk = "Disk space: \nTotal: " + str(output[9].decode("utf-8")) + "\nUsed: " + str(output[10].decode("utf-8")) + " (" + str(output[12].decode("utf-8")) + ")\nFree: " + str(output[11].decode("utf-8"))
		temp = "Raspberry temperature: " + str(t) + "°C"
		message = temp + "\n\n" + disk
		bot.sendMessage(chat_id = chat_id, text = message)
	else:
		update.message.reply_text("not allowed.")


def main():

	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler('status', status))

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()