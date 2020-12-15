import telebot, requests

bot_token = telebot.TeleBot('1411898629:AAHtO0bDuU1jLOfKaTANq3ssiJdI9_Km6wQ')
bot_name = '@Mymrik_bot'
bot_url = url = "https://api.telegram.org/bot{token}/sendMessage".format(token=bot_token)
users = {'Ksenia': 354189613, 'Irina': 689601226}

def do_something():
	print(users)


if __name__ == "__main__":
	# @bot_token.message_handler(commands=['start'])
	# def start_message(message):
	# 	bot_token.send_message(message.chat.id, 'Привет, ты написал мне /start')
	for person in users:
		bot_token.send_message(users.get(person), 'Simple text')

	# bot_token.polling()
