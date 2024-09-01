import requests
from concurrent.futures import ThreadPoolExecutor
import time

access_token = '' # https://vkhost.github.io/
owner_id = -187917017
album_id = -7
offset = 0
count = 200

url = 'https://api.vk.com/method/photos.get'

def download_image(photo_data):
    """Downloads an image from a given URL and saves it with the desired filename."""
    url = photo_data['url']
    filename = photo_data['filename']
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

while True:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Requesting photos from offset {offset}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    params = {
        'access_token': access_token,
        'owner_id': owner_id,
        'album_id': album_id,
        'offset': offset,
        'count': count,
        'v': '5.131'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        photos = data['response']['items']

        def determine_max_photo_res(item):
            sizes = []
            for size in item['sizes']:
                sizes.append(size['type'])
            if 'w' in sizes:
                return item['sizes'][sizes.index('w')]['url']
            elif 'z' in sizes:
                return item['sizes'][sizes.index('z')]['url']
            elif 'y' in sizes:
                return item['sizes'][sizes.index('y')]['url']
            elif 'x' in sizes:
                return item['sizes'][sizes.index('x')]['url']
            elif 'm' in sizes:
                return item['sizes'][sizes.index('m')]['url']
            elif 's' in sizes:
                return item['sizes'][sizes.index('s')]['url']
        
        # Create a list of dictionaries, each containing the url and filename
        photos_to_download = [{'url': determine_max_photo_res(photo), 'filename': f"photo-{abs(photo['owner_id'])}_{photo['id']}.jpg"} for photo in photos]

        # Download images concurrently
        with ThreadPoolExecutor() as executor:
            executor.map(download_image, photos_to_download)

        offset += count

        print("Sleeping 10 seconds")

        # Wait ten seconds before proceeding
        time.sleep(10)

    else:
        print('Error:', response)
        print(response.json())
        break  # Exit the loop if there's an error
