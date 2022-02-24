import requests

with open('Secrets.txt', 'r') as f:
    secret_data = eval(f.read())

users = secret_data.get('users')
secret_password = secret_data.get('secret_password')
time = 10
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


def search(site):
    try:
        r = requests.get(site['url'], headers=headers, cookies=site['Cookie'])

        with open("r1.html", "w", encoding="utf-8") as f:
            f.write(r.text)

        assert (r.status_code == 200)
    except:
        raise AssertionError(f'Ошибка при открытии страницы {site["url"]}')
    else:
        if not site['Search']:
            for no in site['no']:
                result = True if r.text.find(no) == -1 else False  # Не найдет, если есть в наличии
        else:
            result = True if r.text.find(site['Search']) != -1 else False  # Не найдет, если нет в наличии

            if r.text.find(site['name']) == -1:
                raise SystemError(f'Нет названия {site["name"]} на странице {site["url"]}.')
            else:
                if result:
                    raise Warning(f'{site["name"]} появился!\n {site["url"]}.')


if __name__ == "__main__":
    # Simple ugly test
    example = {'name': 'Сталево',
               'url': 'https://apteka.ru/product/stalevo-0050012502-n30-tabl-pplenoboloch-5e32775aca7bdc0001934127/',
               'Search': False, 'no': ['Товара нет в наличии'],
               'Cookie': {'__ddg3': 'bVwJR3is1jg9ow9e', 'pipeline-id': '227969870', '__ddg1': 'EEmsSn0q7FSxdzMyC7Ph',
                          'authToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZGM0MTgyYS03M2E4LTBlODQtZTJiZi0zMWU5ZjVlMzc1MDIiLCJqdGkiOiI1ZmQwZTU5NzNhM2E5MzAwMDE3OGNiNDciLCJleHAiOjE2MjMwNzc3ODMsIm5iZiI6MTYwNzUyNTc4Mywicm9sZSI6IlNoYWRvd1VzZXIiLCJpYXQiOjE2MDc1MjU3ODN9.QJObsnn5lniH94S8Dim-CL2qTsQzi2w45LBey9Jc0qmoysNUPi8T7-EwXul9Ge_ElcrkroOJVFxmdfxQBoas0AUv_pj9sG9pJQ-A4wNr8Psy8pjrXJriU2-nFBpLDYlg0AHFI564rbErHmWDrcIrQKNs4wOpbvDG_ao5drRKFoot18ziKMDOWKKHbXGWWTJ9b6MbDZiLW9Vs8wCEF7a4W0Y43nAke_pg-uaSU9lOiQn1OrRrFQj7hz97gaAnKeSfR3C2NJTvTPYpcywP0wyaOCHIROv29mCCXt7ID6FgBYwmGnQpVS7h1NMVnL8i26ra2MPMkDkxZHUY_zqECQy6mnS2XAoFGbJezCkHd38CPniJB6SniC6nQgPCLMtBEptFKp-SVjtxtK5eAAg7oDEjLt0IWDSINnxsiCa00JLEHk2ff_rJFskvke3-oLdOmIMTguBgx1-raVKK1EReMVhDz4IL9TvcSge6aH41n5V4ThDEJf9ciWSlqZFI-Q1YLBPuMK5V0Gc-Fn778B3s4Aqha5iXegEjf2Sj2QkOpu7vh2XZJB0d6Srbj_twfR8beXK7T1cngE6_x_tcJJtmLxT72s_Uu8HBaC4xXrhsOjpzb3AbXOz4Umz2g3T4So6On_0h_3gSDy6HJUgdpjqpO1-Lw_K_Xx72zpwRyMWPf7HRNKY',
                          'sessionId': 'ddc4182a-73a8-0e84-e2bf-31e9f5e37502', '__ddg2': 'IxqweLUKIIidejOm'}}

    try:
        search(example)
    except SystemError as e:
        print("1, ", e)
    except AssertionError as e:
        print("3, ", e)
    except Warning as e:
        print("2, ", e)
