import requests
import os
import file_functions
from requests import HTTPError
from dotenv import load_dotenv


def download_image_by_id(image_id, download_path):
    url = 'http://hubblesite.org/api/v3/image/{}'.format(image_id)
    response = requests.get(url)
    response.raise_for_status()
    image = response.json().get('image_files')[-1]
    file_url = 'https:{}'.format(image.get('file_url'))
    file_name = f'{image_id}{file_functions.get_file_extension(file_url)}'
    file_functions.download_file(file_url, file_name, download_path)


def download_collection(collection, download_path):
    response = requests.get('https://hubblesite.org/api/v3/images/{}'.format(collection))
    response.raise_for_status()
    images = response.json()
    for image in images:
        download_image_by_id(image['id'], download_path)


if __name__ == '__main__':
    load_dotenv()
    download_path = file_functions.make_dir(os.getenv('DOWNLOAD_FOLDER'))
    try:
        download_collection('holiday_cards', download_path)
    except HTTPError:
        print('Ошибка при загрузке файла')
