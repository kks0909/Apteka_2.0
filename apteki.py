import requests


def search(site):
	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'cache-control': 'max-age=0',
		'dnt': '1',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

	r = requests.get(site['url'], headers=headers, cookies=site['Cookie'])
	if not site['Search']:
		result = True if r.text.find(site['no']) == -1 else False  # Не найдет, если есть в наличии
	else:
		result = False if r.text.find(site['Search']) == -1 else True  # Не найдет, если нет в наличии

	with open("r1.html","w",encoding="utf-8") as f:
		f.write(r.text)

	if r.text.find(site['name']) == -1:
		raise SystemError('Бот сломался.')
	else:
		if result:
			raise Exception('{} появился!\n {}'.format(site['name'], site['url']))


if __name__ == "__main__":
	example = {'name': 'Сталево', 'url': 'https://stolichki.ru/drugs/stalevo-tab-50mg-12-5mg-200mg-30', 'Search': False, 'no': 'Товара нет в наличии', 'Cookie': {'cityId': '77', 'cityChosen': '1'}}
	try:
		search(example)
	except SystemError as e:
		print("1")
	except Exception as e:
		print("2")

#
# with open("r2.html","w",encoding="utf-8") as f:
#     f.write(r.text)
