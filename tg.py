import telebot, pickle
from apteki import search
from time import sleep
from threading import Thread, Event
from functools import reduce

# TODO Автозапуск
# TODO Лог изменений

bot = telebot.TeleBot('1411898629:AAHtO0bDuU1jLOfKaTANq3ssiJdI9_Km6wQ')
admin = 354189613
new_user = {}
new_source = {'name': None, 'url': None, 'Search': False, 'no': False, 'Cookie': None}
removing_source = None
WORK = True

with open('data.pickle', 'rb') as f:
	load_data = pickle.load(f)

users = load_data[0]
time = int(load_data[1])
secret_password = load_data[2]
base = load_data[3]

def clear_new_source():
	global new_source
	new_source = {'name': None, 'url': None, 'Search': False, 'no': False, 'Cookie': None}


def repeated_search():
	while True:
		while WORK:
			for site in base:
				try:
					search(site)
				except SystemError as e:
					bot.send_message(admin, e)
					print("1")
				except Exception as e:
					print("2")
					for person in users:
						bot.send_message(users.get(person), e)
				print('*')
			# event.wait(time)
			sleep(time * 60)
		sleep(5)


def check_new_source(message):
	try:
		search(new_source)
	except SystemError as e:
		bot.send_message(message.chat.id, 'Ошибка: {}'.format(e))
	except Exception as e:
		bot.send_message(message.chat.id, e)
	bot.send_message(message.chat.id, 'Вы добавили новый источник.')
	clear_new_source()


def write_new_data():
	with open('data.pickle', 'wb') as f:
		pickle.dump([users, time, secret_password, base], f)


@bot.message_handler(commands=['start'])
def start_message(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	keyboard.add('Добавиться', 'Изменить время опроса', 'Вывести список источников', 'Добавить источник', 'Удалить источник', 'Приостановить', 'Запустить')
	bot.send_message(message.chat.id, '?', reply_markup=keyboard)


@bot.message_handler()
def reply(message):

	if message.chat.id in users.values():
		if message.text == 'Добавиться':
			bot.send_message(message.chat.id, 'Вы уже зарегистрированный пользователь.')
		elif message.text == 'Изменить время опроса':
			bot.send_message(message.chat.id, 'Текущее время опроса:\n{}'.format(time))
			bot.send_message(message.chat.id, 'Введите время в минутах:')
			bot.register_next_step_handler(message, new_time)
		elif message.text == 'Вывести список источников':
			bot.send_message(message.chat.id, reduce(lambda s1, s2: s1 + s2, list(map(lambda item: '{}\n{}\n\n'.format(item['name'], item['url']), base))))
		elif message.text == 'Добавить источник':
			bot.send_message(message.chat.id, 'Введите название:')
			bot.register_next_step_handler(message, new_source_name)
		elif message.text == 'Удалить источник':
			bot.send_message(message.chat.id, reduce(lambda s1, s2: s1 + s2, list(map(lambda x: '{}) {}'.format(x[0] + 1, x[1]), list(enumerate(list(map(lambda item: '{}\n{}\n\n'.format(item['name'], item['url']), base))))))))
			bot.register_next_step_handler(message, remove_source)
		elif message.text == 'Приостановить':
			global WORK
			WORK = False
			print(WORK)
		elif message.text == 'Запустить':
			# global WORK
			WORK = True
			print(WORK)
		else:
			bot.send_message(message.chat.id, 'Введена неверная команда, либо у Вас нет прав на совершение действия.')

		if message.chat.id == admin:
			if message.text == 'Изменить пароль':
				bot.send_message(admin, 'Введите новый пароль:')
				bot.register_next_step_handler(message, change_password)
	else:
		if message.text == 'Добавиться':
			bot.send_message(message.chat.id, 'Введите пароль:')
			bot.register_next_step_handler(message, input_pass)
		else:
			bot.send_message(message.chat.id, 'Вы не зарегистрированный пользователь')


def input_pass(message):
	if message.text == secret_password:
		bot.send_message(message.chat.id, 'Введите имя:')
		bot.register_next_step_handler(message, get_name)
	else:
		bot.send_message(message.chat.id, 'Неверный пароль')


def get_name(message):
	global new_user
	new_user = {message.text: message.from_user.id}
	# Спрашиваем разрешение у админа
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text="Yes", callback_data="new_user_yes"))
	markup.add(telebot.types.InlineKeyboardButton(text="No", callback_data="new_user_no"))
	bot.send_message(admin, text='Запрос на добавление:\n{}'.format(new_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if call.data == 'new_user_yes':
		users.update(new_user)
		write_new_data()
		bot.send_message(admin, 'Все пользователи:\n{}'.format(users))
	if call.data == 'new_user_no':
		bot.send_message(new_user.popitem()[1], 'Авторизация отклонена.')
	if call.data == 'url_to_end_page':
		bot.send_message(call.message.chat.id, 'Введите признак отсутствия:\n(например, "Товар закончился" или "Сообщить о поступлении")')
		bot.register_next_step_handler(call.message, input_no)
	if call.data == 'url_to_list':
		bot.send_message(call.message.chat.id, 'Введите ключ поиска:\n(например, "150мг" или "Алси")')
		bot.register_next_step_handler(call.message, input_search)
	if call.data == 'new_source_yes':
		base.append(new_source)
		write_new_data()
		bot.send_message(call.message.chat.id, 'Проверка нового источника.')
		bot.register_next_step_handler(call.message, check_new_source)
	if call.data == 'new_source_no':
		bot.send_message(call.message.chat.id, 'Запрос отклонен.')
		clear_new_source()
	if call.data == 'remove_source_yes':
		base.pop(removing_source)
		bot.send_message(call.message.chat.id, 'Вы удалили источник.')
	if call.data == 'remove_source_no':
		bot.send_message(call.message.chat.id, 'Запрос отклонен.')


def new_time(message):
	if message.text.isnumeric():
		global time
		time = int(message.text)
		write_new_data()
		bot.send_message(message.chat.id, 'Вы изменили интервал опроса. \nТекущий: {}'.format(time))
		bot.send_message(admin, 'Был изменен интервал опроса пользователем {}. \nТекущий: {}'.format(message.from_user.first_name, time))
		print(time)
	elif message.text == 'N':
		bot.register_next_step_handler(message, start_message)
	else:
		bot.send_message(message.chat.id, 'Цифрами, пожалуйста:\nЕсли Вы не хотите изменять время, введите N.')
		bot.register_next_step_handler(message, new_time)


def new_source_name(message):
	global new_source
	new_source['name'] = message.text
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text="Конечная", callback_data="url_to_end_page"))
	markup.add(telebot.types.InlineKeyboardButton(text="На список", callback_data="url_to_list"))
	bot.send_message(message.chat.id, text='Ссылка ведет на страницу препарата или на список препаратов?', reply_markup=markup)


def input_no(message):
	global new_source
	new_source['no'] = message.text
	bot.send_message(message.chat.id, 'Вставьте ссылку:')
	bot.register_next_step_handler(message, input_url)


def input_search(message):
	global new_source
	new_source['Search'] = message.text
	bot.send_message(message.chat.id, 'Вставьте ссылку:')
	bot.register_next_step_handler(message, input_url)


def input_url(message):
	global new_source
	new_source['url'] = message.text
	# Спрашиваем правильность введения
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="new_source_yes"))
	markup.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data="new_source_no"))
	bot.send_message(message.chat.id, text='Проверьте правильность введенных данных. Вы добавляете:\n{}\n{}\n{}\n{}'.format(new_source['name'], new_source['url'], new_source['Search'], new_source['no']), reply_markup=markup)


def remove_source(message):
	if message.text.isnumeric() and int(message.text) <= len(base):
		print(int(message.text), len(base))
		global removing_source
		removing_source = int(message.text) - 1
		bot.send_message(message.chat.id, 'Вы удаляете {}?'.format(base[removing_source]['url']))
		# Спрашиваем подтверждение удаления
		markup = telebot.types.InlineKeyboardMarkup()
		markup.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="remove_source_yes"))
		markup.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data="remove_source_no"))
		bot.send_message(message.chat.id, text='Подтверждаю', reply_markup=markup)
	elif message.text == 'N':
		bot.register_next_step_handler(message, start_message)
	else:
		bot.send_message(message.chat.id, 'Цифрами, пожалуйста:\nЕсли Вы не хотите удалять, введите N.')
		bot.register_next_step_handler(message, remove_source)


def change_password(message):
	global secret_password
	secret_password = message.text
	write_new_data()
	bot.register_next_step_handler(message, start_message)


if __name__ == "__main__":
	bot.send_message(admin, 'Бот перезапущен')
	event = Event()
	p2 = Thread(target=bot.polling)
	p1 = Thread(target=repeated_search)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
