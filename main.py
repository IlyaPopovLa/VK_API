import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(url, token):
    api_url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        'access_token': token,
        'v': '5.199',
        'url': url
    }

    try:

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        result = response.json()

        if 'response' in result:
            return result['response']['short_url'], None
        else:
            return None, result['error']['error_msg']

    except Exception as e:
        return None, f"Ошибка ссылки {e}"


def count_clicks(link, token):
    api_url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link,
        'interval': 'forever',
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        result = response.json()

        if 'response' in result:
            return result['response']['stats'][0]['views'], None
        else:
            return None, result['error']['error_msg']
    except Exception as e:
        return None, f"Ошибка статистики кликов {e}"

def is_shorten_link(url):
    parsed = urlparse(url)
    return parsed.netloc in ['vk.cc', 'vk.com']


def main():
    load_dotenv()
    url = input('Введите ссылку: ')
    token = os.getenv("VK_TOKEN")

    if is_shorten_link(url):
        link = urlparse(url).path.lstrip('/')
        clicks, error = count_clicks(link, token)

        if error:
            print(f"Ошибка: {error}")
        else:
            print(f"Короткая ссылка: {url}")
            print(f"Количество кликов: {clicks}")
    else:
        short_url, error = shorten_link(url, token)

        if error:
            print(f"Ошибка: {error}")
            return
        print(f"Сокращенная ссылка: {short_url}")

        link = urlparse(short_url).path.lstrip('/')
        clicks, error = count_clicks(link, token)

        if error:
            print(f"Ошибка: {error}")
            return
        else:
            print(f"Колличество кликов: {clicks}")


if __name__ == "__main__":
    main()