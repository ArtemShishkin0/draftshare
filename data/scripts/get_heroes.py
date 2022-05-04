import shutil, requests, os.path, json, datetime
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

print('Connecting to heroes page...')
req = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json")
print('Github heroes page status:', req)
data = json.loads(req.content)


print('Writing lines...')
with open('../lists/heroes_list.py', 'w') as file:
    file.write(f'#{datetime.datetime.now().strftime("%Y/%m/%d")}\n')
    file.write('heroes_list={\n')
    for x in data:
        try:
            file.write(f"   {x}: ")
            file.write("{")
            file.write(f'"{data[x]["localized_name"]}": "{data[x]["img"]}"')
            file.write("},\n")
        except Exception as Err:
            print(Err, x)
    file.write('}')

print('Writing finished!')
print("Checking for new heroes...")
print('Checking finished!')

def download_images(data):
    for val in data:
        if not os.path.exists(f'{BASE_DIR}/images/heroes/h{val}.png'):
            print(data[val]['localized_name'], "does not exist!", end='')
            print(' Getting image... ', end='')
            url = f'https://cdn.cloudflare.steamstatic.com{data[val]["img"]}'
            response = requests.get(url, stream=True)
            with open(f'../images/heroes/h{val}.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print('Image saved!')
    print('Downloading finished!')

download_images(data)
