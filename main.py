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

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    shorten_link_result = response.json()

    if 'response' in shorten_link_result:
        return shorten_link_result['response']['short_url'], None
    return shorten_link_result['error']['error_msg'], None


def count_clicks(link, token):
    api_url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': token,
        'v': '5.199',
        'key': link,
        'interval': 'forever',
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    count_clicks_result = response.json()

    if 'response' in count_clicks_result and count_clicks_result['response']['stats']:
        return count_clicks_result['response']['stats'][0]['views']
    return None


def is_shorten_link(url, token):
    api_url = "https://api.vk.com/method/utils.checkLink"
    params = {
        'access_token': token,
        'v': '5.199',
        'url': url
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    is_shorten_link_result = response.json()

    if 'response' in is_shorten_link_result:
        return is_shorten_link_result['response'].get('status') == 'not_banned'
    return None


def main():
    load_dotenv()
    url = input('Введите ссылку: ').strip()
    token = os.environ.get("VK_TOKEN")

    try:
        url_components = urlparse(url)
        if url_components.netloc.endswith('vk.cc'):
            link_key = url_components.path.lstrip('/')
            short_url = url
        else:
            short_url, error = shorten_link(url, token)
            if error:
                print(f"Ошибка при сокращении: {error}")
                return
            link_key = urlparse(short_url).path.lstrip('/')

        clicks = count_clicks(link_key, token)

        print(f"Сокращенная ссылка: {short_url}")
        print(f"Количество кликов: {clicks if clicks is not None else 'статистика недоступна'}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")


if __name__ == "__main__":
    main()