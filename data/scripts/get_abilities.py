import json
import datetime
import os
import shutil
import time
import requests
from pathlib import Path
import argparse
BASE_DIR = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description='Get ability images. Modes: normal(default), slow')
parser.add_argument('-m', default='normal')
args = parser.parse_args()
if args.m == 'slow':
    print('Entering in slow mode...')

print()
print('Connecting to abilities page...')
req = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/ability_ids.json")
print('Github abilities page status:', req)
data = json.loads(req.content)

print('Writing lines...')
with open('../lists/abilities_list.py', 'w') as file:
    file.write(f'#{datetime.datetime.now().strftime("%Y/%m/%d")}\n')
    file.write('ability_list={\n')
    for x in data:
        try:
            file.write(f"   {x}: '{data[x]}', \n")
        except Exception as Err:
            print(Err, x)
    file.write('}')

print('Writing finished!')

print('Making a reversed list')
with open('../lists/abilities_list_reversed.py', 'w') as file:
    file.write(f'#{datetime.datetime.now().strftime("%Y/%m/%d")}\n')
    file.write('ability_list_reversed={\n')
    for x in data:
        try:
            file.write(f"   '{data[x]}': {x}, \n")
        except Exception as Err:
            print(Err, x)
    file.write('}')

print('Reversed list writing finished!')

def download_images(data):
    for x in data:
        if 'special_' not in data[x] and 'roshan_' not in data[x] and 'greevil_' and 'seasonal_':
            if not os.path.exists(f'{BASE_DIR}/images/abilities/{data[x]}.png'):
                print(data[x], "does not exist - trying to download...")
                if args.m == 'normal':
                    url1 = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/abilities/{data[x]}_lg.png'
                    url2 = f'https://cdn.datdota.com/images/ability/{data[x]}.png'
                    response1 = requests.get(url1, stream=True)
                    response2 = requests.get(url2, stream=True)
                elif args.m == 'slow':
                    url2 = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/abilities/{data[x]}_lg.png'
                    url1 = f'https://cdn.datdota.com/images/ability/{data[x]}.png'
                    response1 = requests.get(url1, stream=True)
                    time.sleep(1)
                    response2 = requests.get(url2, stream=True)
                #https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/abilities/zuus_heavenly_jump.png
                if response1.status_code != 200 and response2.status_code != 200:
                    print('No image data found')
                elif response1.status_code == 200:
                    with open(f'../images/abilities/{data[x]}.png', 'wb') as out_file:
                        shutil.copyfileobj(response1.raw, out_file)
                    del response1
                    print(f'Created {data[x]} - through steamstatic.com') if args.m != 'slow' else print(f'Created {data[x]} - through datdota.com')
                elif response2.status_code == 200:
                    with open(f'../images/abilities/{data[x]}.png', 'wb') as out_file:
                        shutil.copyfileobj(response2.raw, out_file)
                    del response2
                    print(f'Created {data[x]} - through datdota.com') if args.m != 'slow' else print(f'Created {data[x]} - through steamstatic.com')
    print('Downloading done!')
download_images(data)