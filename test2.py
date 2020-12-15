from functools import reduce
from test import do_something
import pickle

users = {'Ksenia': 354189613, 'Irina': 689601226}
time = 10
secret_password = 'ParentsT'
base = [{'name': 'Сталево', 'url': 'https://apteka.ru/product/stalevo-0050012502-n30-tabl-pplenoboloch-5e32775aca7bdc0001934127/', 'Search': False, 'no': 'Товара нет в наличии', 'Cookie': {'__ddg3': 'bVwJR3is1jg9ow9e', 'pipeline-id': '227969870', '__ddg1': 'EEmsSn0q7FSxdzMyC7Ph', 'authToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZGM0MTgyYS03M2E4LTBlODQtZTJiZi0zMWU5ZjVlMzc1MDIiLCJqdGkiOiI1ZmQwZTU5NzNhM2E5MzAwMDE3OGNiNDciLCJleHAiOjE2MjMwNzc3ODMsIm5iZiI6MTYwNzUyNTc4Mywicm9sZSI6IlNoYWRvd1VzZXIiLCJpYXQiOjE2MDc1MjU3ODN9.QJObsnn5lniH94S8Dim-CL2qTsQzi2w45LBey9Jc0qmoysNUPi8T7-EwXul9Ge_ElcrkroOJVFxmdfxQBoas0AUv_pj9sG9pJQ-A4wNr8Psy8pjrXJriU2-nFBpLDYlg0AHFI564rbErHmWDrcIrQKNs4wOpbvDG_ao5drRKFoot18ziKMDOWKKHbXGWWTJ9b6MbDZiLW9Vs8wCEF7a4W0Y43nAke_pg-uaSU9lOiQn1OrRrFQj7hz97gaAnKeSfR3C2NJTvTPYpcywP0wyaOCHIROv29mCCXt7ID6FgBYwmGnQpVS7h1NMVnL8i26ra2MPMkDkxZHUY_zqECQy6mnS2XAoFGbJezCkHd38CPniJB6SniC6nQgPCLMtBEptFKp-SVjtxtK5eAAg7oDEjLt0IWDSINnxsiCa00JLEHk2ff_rJFskvke3-oLdOmIMTguBgx1-raVKK1EReMVhDz4IL9TvcSge6aH41n5V4ThDEJf9ciWSlqZFI-Q1YLBPuMK5V0Gc-Fn778B3s4Aqha5iXegEjf2Sj2QkOpu7vh2XZJB0d6Srbj_twfR8beXK7T1cngE6_x_tcJJtmLxT72s_Uu8HBaC4xXrhsOjpzb3AbXOz4Umz2g3T4So6On_0h_3gSDy6HJUgdpjqpO1-Lw_K_Xx72zpwRyMWPf7HRNKY', 'sessionId': 'ddc4182a-73a8-0e84-e2bf-31e9f5e37502', '__ddg2': 'IxqweLUKIIidejOm'}},
		{'name': 'Сталево', 'url': 'https://stolichki.ru/drugs/stalevo-tab-50mg-12-5mg-200mg-30', 'Search': False, 'no': 'Товара нет в наличии', 'Cookie': {'cityId': '77', 'cityChosen': '1'}},
		{'name': 'Сталево', 'url': 'https://ozerki.ru/catalog/?q=%D1%81%D1%82%D0%B0%D0%BB%D0%B5%D0%B2%D0%BE', 'Search': '12,5', 'no': False, 'Cookie': {'IWEB_CITY': '20238', 'SELECTED_CITY': '20238'}},
		{'name': 'Сталево', 'url': 'https://apteka.marata41.ru/catalog/parkinson/stalevo-tabletki-50mg-12-5mg-200mg-30/', 'Search': False, 'no': 'Сообщить о поступлении', 'Cookie': None},
		{'name': 'Сталево', 'url': 'https://aptekanevis.ru/catalog/poisk-preparata.php?q=%D1%81%D1%82%D0%B0%D0%BB%D0%B5%D0%B2%D0%BE&s=', 'Search': ' 50мг', 'no': False, 'Cookie': {'region': '1'}}]

print(len(base))
base.pop(3)
print(len(base))
print('Wow, new changes!')
do_something()

with open('data.pickle', 'wb') as f:
	pickle.dump([users, time, secret_password, base], f)

with open('data.pickle', 'rb') as f:
	data_new = pickle.load(f)


print(data_new[1])
