import datetime
import json
import os
import shutil
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent.parent

print('Connecting to items page...')
req = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/items.json")
print('Github items page status:', req)
data = json.loads(req.content)

print('Writing lines...')
with open('../lists/item_list.py', 'w') as file:
    file.write(f'#{datetime.datetime.now().strftime("%Y/%m/%d")}\n')
    file.write('item_list={\n')
    for x in data:
        try:
            file.write(f"   {data[x]['id']}: '{data[x]['img']}', \n")

        except Exception as Err:
            print(Err, x)
    file.write('}')

print('Writing finished!')
def download_images(data):
    for x in data:
            if not os.path.exists(f'{BASE_DIR}/images/items/{data[x]["id"]}.png'):
                print(data[x]["id"], "does not exist... ",end='')
                url = f'https://cdn.cloudflare.steamstatic.com/{data[x]["img"]}'
                response = requests.get(url, stream=True)
                if response.status_code != 200:
                    print('No image data found on the server')
                elif response.status_code == 200:
                    with open(f'../images/items/{data[x]["id"]}.png', 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
                    print(f'Created {data[x]["id"]} - through steamstatic.com')
    print('Downloading done!')
download_images(data)
