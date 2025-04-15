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


def is_shorten_link(url):
    parsed = urlparse(url)
    # Проверяем, что путь состоит из короткого идентификатора (например, 1-6 символов)
    path = parsed.path.lstrip('/')
    return len(path) <= 6 and path.isalnum()


def main():
    load_dotenv()
    url = input('Введите ссылку: ')
    token = os.environ["VK_TOKEN"]

    if is_shorten_link(url):
        link = urlparse(url).path.lstrip('/')
        try:
            clicks = count_clicks(link, token)
            print(f"Короткая ссылка: {url}")
            print(f"Количество кликов: {clicks}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе статистики: {e}")
    else:
        try:
            short_url, error = shorten_link(url, token)
            if error:
                print(f"Ошибка: {error}")
                return

            print(f"Сокращенная ссылка: {short_url}")
            link = urlparse(short_url).path.lstrip('/')
            clicks = count_clicks(link, token)
            print(f"Количество кликов: {clicks}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при сокращении ссылки: {e}")


if __name__ == "__main__":
    main()