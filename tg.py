import telebot, pickle, logging
from apteki import search
from time import sleep
from threading import Thread, Event
from functools import reduce
from datetime import datetime, date

# TODO Лог изменений
# TODO https://www.acmespb.ru/preparaty/stalevo/4607018262084 Увеличение наименования

logging.basicConfig(filename=f'Logs\{date.today()}.txt', filemode='a', level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%H:%M:%S')
bot = telebot.TeleBot('1411898629:AAHtO0bDuU1jLOfKaTANq3ssiJdI9_Km6wQ')
admin = 354189613
new_user = {}
new_source = {'name': None, 'url': None, 'Search': False, 'no': False, 'Cookie': None}
removing_source = None
removing_user = None
sender = None
WORK = True
last_search_time = 0

with open('data.pickle', 'rb') as f:
	load_data = pickle.load(f)

users = load_data[0]
time = int(load_data[1])
secret_password = load_data[2]
base = load_data[3]


def clear_new_source():
	global new_source
	new_source = {'name': None, 'url': None, 'Search': False, 'no': False, 'Cookie': None}
	logging.info('Очистка поля нового источника.')


def repeated_search():
	while True:
		while WORK:
			i = 0
			for site in base:
				try:
					search(site)
				except SystemError as e:
					bot.send_message(admin, e)
					logging.warning(e)
				except Warning as e:
					for person_id in users:
						bot.send_message(person_id, e)
					logging.warning(e)
				except AssertionError as e:
					bot.send_message(admin, e)
					logging.warning(e)
				else:
					i += 1
			print(datetime.now(), i)
			global last_search_time
			last_search_time = datetime.now()
			# event.wait(time)
			sleep(time * 60)
		sleep(5)


def check_new_source():
	try:
		search(new_source)
	except SystemError as e:
		logging.info(f'Ошибка при добавлении нового источника пользователем {users.get(sender)}({sender}).\n Ошибка: {e}')
		bot.send_message(sender, f'Ошибка: {e}')
	except Warning as e:
		logging.info(f'Ошибка при добавлении нового источника пользователем {users.get(sender)}({sender}).\n Ошибка: {e}')
		bot.send_message(sender, e)
	except AssertionError as e:
		logging.info(f'Ошибка при добавлении нового источника пользователем {users.get(sender)}({sender}).\n Ошибка: {e}')
		bot.send_message(sender, e)
	else:
		logging.info(f'Проверка пройдена.\nДобавление нового источника {new_source["url"]} пользователем {users.get(sender)}({sender}).')
		bot.send_message(sender, 'Вы добавили новый источник.')
	finally:
		clear_new_source()


def write_new_data():
	with open('data.pickle', 'wb') as f:
		pickle.dump([users, time, secret_password, base], f)
	logging.info('Обновление базы.')


@bot.message_handler(commands=['start'])
def start_message(message):
	logging.info('Открытие бота /start.')
	keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	keyboard.add('Добавиться', 'Изменить время опроса', 'Вывести время последнего опроса', 'Вывести список источников', 'Добавить источник', 'Удалить источник', 'Приостановить', 'Запустить')
	bot.send_message(message.chat.id, '?', reply_markup=keyboard)


@bot.message_handler()
def reply(message):
	if message.chat.id in users.keys():
		if message.text == 'Добавиться':
			logging.info(f'Попытка опять зарегистрироваться пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, 'Вы уже зарегистрированный пользователь.')
		elif message.text == 'Изменить время опроса':
			logging.info(f'Попытка изменить время опроса пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, f'Текущее время опроса:\n{time}')
			bot.send_message(message.chat.id, 'Введите новое время в минутах:\n (не 0)')
			bot.register_next_step_handler(message, new_time)
		elif message.text == 'Вывести время последнего опроса':
			logging.info(f'Запрос времени последнего опроса пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, f'Последний опрос:\n{last_search_time}')
		elif message.text == 'Вывести список источников':
			logging.info(f'Запрос списка источников пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, reduce(lambda s1, s2: s1 + s2, list(map(lambda item: f"{item['name']}\n{item['url']}\n\n", base))))
		elif message.text == 'Добавить источник':
			logging.info(f'Попытка добавить новый источник пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, 'Введите название:')
			bot.register_next_step_handler(message, new_source_name)
		elif message.text == 'Удалить источник':
			logging.info(f'Попытка удалить источник пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, reduce(lambda s1, s2: s1 + s2, list(map(lambda x: f'{x[0] + 1}) {x[1]}', list(enumerate(list(map(lambda item: f"{item['name']}\n{item['url']}\n\n", base))))))))
			bot.register_next_step_handler(message, remove_source)
		elif message.text == 'Приостановить':
			global WORK
			WORK = False
			logging.warning(f'Остановка бота пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(admin, f'Остановка бота пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
		elif message.text == 'Запустить':
			# global WORK
			WORK = True
			logging.warning(f'Запуск бота пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(admin, f'Запуск бота пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
		elif message.chat.id == admin:
			if message.text == 'Admin':
				logging.info('Открытие админской панели.')
				markup = telebot.types.InlineKeyboardMarkup()
				markup.add(telebot.types.InlineKeyboardButton(text='Изменить пароль', callback_data='change_password'))
				markup.add(telebot.types.InlineKeyboardButton(text='Показать пользователей', callback_data='show_users'))
				markup.add(telebot.types.InlineKeyboardButton(text='Удалить пользователя', callback_data='remove_user'))
				markup.add(telebot.types.InlineKeyboardButton(text='Прислать лог', callback_data='send_log'))
				bot.send_message(admin, text='?', reply_markup=markup)
		else:
			logging.info(f'Ввод неверной команды: {message.text} пользователем {users.get(message.chat.id)}({message.chat.first_name}).')
			bot.send_message(message.chat.id, 'Введена неверная команда, либо у Вас нет прав на совершение действия.')



	else:
		if message.text == 'Добавиться':
			logging.info(f'Попытка зарегистрироваться пользователем {message.chat.first_name}({message.chat.id}).')
			bot.send_message(message.chat.id, 'Введите пароль:')
			bot.register_next_step_handler(message, input_pass)
		else:
			logging.info(f'Попытка совершения действия незарегистрированным пользователем {message.chat.first_name}({message.chat.id}).')
			bot.send_message(message.chat.id, 'Вы не зарегистрированный пользователь')


def input_pass(message):
	if message.text == secret_password:
		logging.info(f'Ввод правильного пароля незарегистрированным пользователем {message.chat.first_name}({message.chat.id}).')
		bot.send_message(message.chat.id, 'Введите имя:')
		bot.register_next_step_handler(message, get_name)
	else:
		logging.info(f'Ввод неправильного пароля: {message.text} незарегистрированным пользователем {message.chat.first_name}({message.chat.id}).')
		bot.send_message(message.chat.id, 'Неверный пароль')


def get_name(message):
	global new_user
	new_user = {message.chat.id: message.text}
	# Спрашиваем разрешение у админа
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text="Yes", callback_data="new_user_yes"))
	markup.add(telebot.types.InlineKeyboardButton(text="No", callback_data="new_user_no"))
	bot.send_message(admin, text=f'Запрос на добавление:\n{new_user}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if call.data == 'new_user_yes':
		logging.info(f'Подтверждение админом добавления нового пользователя {new_user}.')
		users.update(new_user)
		write_new_data()
		bot.send_message(admin, f'Все пользователи:\n' + reduce(lambda s1, s2: s1 + s2, list(map(lambda item: f'{users.get(item)} ({item})\n', users))))
	elif call.data == 'new_user_no':
		logging.info(f'Отклонение админом добавления нового пользователя {new_user}.')
		bot.send_message(new_user.popitem()[0], 'Авторизация отклонена.')
	elif call.data == 'url_to_end_page':
		bot.send_message(call.message.chat.id, 'Введите признак отсутствия списком:\n(например, "Товар закончился" или "Сообщить о поступлении")')
		logging.info('Ввод признака отсутствия')
		bot.register_next_step_handler(call.message, input_no)
	elif call.data == 'url_to_list':
		bot.send_message(call.message.chat.id, 'Введите ключ поиска:\n(например, "150мг" или "Алси")')
		logging.info('Ввод ключа поиска')
		bot.register_next_step_handler(call.message, input_search)
	elif call.data == 'new_source_yes':
		base.append(new_source)
		base.append(new_source)
		write_new_data()
		logging.info(f'Проверка нового источника добавленного пользователем {call.message.chat.first_name}({call.message.chat.id}).')
		bot.send_message(call.message.chat.id, 'Проверка нового источника.')
		global sender
		sender = call.message.chat.id
		check_new_source()
	elif call.data == 'new_source_no':
		logging.info(f'Отклонение добавления нового источника {new_source["url"]} пользователем {call.message.chat.first_name}({call.message.chat.id}).')
		bot.send_message(call.message.chat.id, 'Запрос отклонен.')
		clear_new_source()
	elif call.data == 'remove_source_yes':
		logging.info(f'Удаление источника {base[removing_source]["url"]} пользователем {call.message.chat.first_name}({call.message.chat.id}).')
		base.pop(removing_source)
		write_new_data()
		bot.send_message(call.message.chat.id, 'Вы удалили источник.')
	elif call.data == 'remove_source_no':
		logging.info(f'Отклонение удаления источника {base[removing_source]["url"]} пользователем {call.message.chat.first_name}({call.message.chat.id}).')
		bot.send_message(call.message.chat.id, 'Запрос отклонен.')
	elif call.data == 'change_password':
		logging.info('Попытка изменить пароль админом.')
		bot.send_message(admin, 'Введите новый пароль:')
		bot.register_next_step_handler(call.message, change_password)
	elif call.data == 'show_users':
		logging.info('Вывод всех пользователей админом.')
		bot.send_message(admin, reduce(lambda s1, s2: s1 + s2, list(map(lambda item: f'{users.get(item)} ({item})\n', users))))
	elif call.data == 'remove_user':
		logging.info('Попытка удалить пользователя админом.')
		bot.send_message(admin, reduce(lambda s1, s2: s1 + s2, list(map(lambda item: f'{users.get(item)} ({item})\n', users))))
		bot.register_next_step_handler(call.message, remove_user)
	elif call.data == 'send_log':
		with open(f'{date.today()}.txt', 'rb') as log_file:
			bot.send_document(admin, log_file)
	elif call.data == 'remove_user_yes':
		logging.info(f'Удаление пользователя {users.get(removing_user)} админом.')
		users.pop(removing_user)
		write_new_data()
		bot.send_message(admin, 'Вы удалили пользователя.')
	elif call.data == 'remove_user_no':
		logging.info(f'Отклонение удаления пользователя {users.get(removing_user)} админом.')
		bot.send_message(admin, 'Запрос отклонен.')


def new_time(message):
	if message.text.isnumeric() and int(message.text) > 0:
		global time
		time = int(message.text)
		write_new_data()
		bot.send_message(message.chat.id, f'Вы изменили интервал опроса. \nТекущий: {time}')
		bot.send_message(admin, f'Был изменен интервал опроса пользователем {users.get(message.chat.id)}({message.chat.first_name}).\nТекущий: {time}')
		logging.warning(f'Интервал опроса изменен пользователем {users.get(message.chat.id)}({message.chat.first_name}).\nТекущий: {time}')
	elif message.text == 'N':
		logging.info(f'Отмена ввода нового интервала опроса пользователем {users.get(message.chat.id)}({message.chat.first_name}.')
	else:
		logging.info(f'Неудачный ввод нового интервала опроса пользователем {users.get(message.chat.id)}({message.chat.first_name}.')
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
	bot.send_message(message.chat.id, text=f'Проверьте правильность введенных данных. Вы добавляете:\n{new_source["name"]}\n{new_source["url"]}\n{new_source["Search"]}\n{new_source["no"]}.', reply_markup=markup)


def remove_source(message):
	if message.text.isnumeric() and int(message.text) <= len(base):
		global removing_source
		removing_source = int(message.text) - 1
		# Спрашиваем подтверждение удаления
		markup = telebot.types.InlineKeyboardMarkup()
		markup.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="remove_source_yes"))
		markup.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data="remove_source_no"))
		bot.send_message(message.chat.id, text=f'Вы удаляете {base[removing_source]["url"]}?', reply_markup=markup)
	elif message.text == 'N':
		logging.info(f'Отмена удаления источника пользователем {users.get(message.chat.id)}({message.chat.first_name}.')
	else:
		logging.info(f'Неудачный ввод номера удаляемого источника пользователем {users.get(message.chat.id)}({message.chat.first_name}.')
		bot.send_message(message.chat.id, 'Цифрами, пожалуйста:\nЕсли Вы не хотите удалять, введите N.')
		bot.register_next_step_handler(message, remove_source)


def change_password(message):
	global secret_password
	secret_password = message.text
	logging.warning('Изменение пароля админом.')
	bot.send_message(admin, 'Вы поменяли пароль.')
	write_new_data()


def remove_user(message):
	if message.text.isnumeric() and message.chat.id in users.keys():
		global removing_user
		removing_user = int(message.text)
		# Спрашиваем подтверждение удаления
		markup = telebot.types.InlineKeyboardMarkup()
		markup.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="remove_user_yes"))
		markup.add(telebot.types.InlineKeyboardButton(text="Нет", callback_data="remove_user_no"))
		bot.send_message(message.chat.id, text=f'Вы удаляете {users.get(int(message.text))}?', reply_markup=markup)
	elif message.text == 'N':
		logging.info(f'Отмена удаления пользователя {users.get(message.text)} админиом.')
	else:
		logging.info(f'Неудачный ввод id удаляемого пользователя админом.')
		bot.send_message(message.chat.id, 'Цифрами, пожалуйста:\nЕсли Вы не хотите удалять, введите N.')
		bot.register_next_step_handler(message, remove_source)


if __name__ == "__main__":
	bot.send_message(admin, 'Бот запущен')
	logging.warning('Бот запущен')
	event = Event()
	p2 = Thread(target=bot.infinity_polling)
	p1 = Thread(target=repeated_search)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
