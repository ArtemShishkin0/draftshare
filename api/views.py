import io
import os
import shutil
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from api.serializers import DataSerializer
from PIL import Image, ImageDraw, ImageFont
import requests
import json
from data.lists.heroes_list import heroes_list
from data.lists.abilities_list import ability_list
from data.lists.abilities_list_reversed import ability_list_reversed
from data.lists.ult_list import ult_list
apikey = os.environ.get('STEAMAPI_DEV_KEY')


def getplayerattributes(player):
    spells_id = []
    for z in player['ability_upgrades']:
        spells_id.append(z['ability'])
    spells_id = set(spells_id)
    abilities = [ability_list.get(spell) for spell in spells_id if 'special_' not in ability_list.get(spell)]
    # items =
    return abilities

def drawimages(player, abilities, data):
    x, le = 303, 116 #start drawing ability images x-axis and length
    spells_cords = [(x, 18), (x + le * 1, 18), (x + le * 2, 18)]
    ult_cords = [(x + le * 3, 18)]
    hero_model = Image.open(f'./data/images/heroes/h{player["hero_id"]}.png', mode='r')
    if data['result']['radiant_win'] and player['player_slot'] <= 5:
        template = Image.open('./data/images/misc/template_player_win_min.png', mode='r')
    elif not data['result']['radiant_win'] and player['player_slot'] > 6:
        template = Image.open('./data/images/misc/template_player_win_min.png', mode='r')
    else:
        template = Image.open('./data/images/misc/template_player_lose_min.png', mode='r')
    hero_model = hero_model.resize((257, 145))  # 256*144 - basic hero model resolution
    template.paste(hero_model, (29, 18))


    safe = 1
    for i in abilities:
        if ability_list_reversed.get(i) in ult_list:  #need to rework ult list completely -- get ult id from the ulti name list
           safe -= 1

    if safe:    #safe mode if no ult was found
        print(f'PASTING ABILITIES IN SAFE MODE! {abilities}')
        spells_cords = spells_cords + ult_cords
        for i in range(4):
            ability = Image.open(f'./data/images/abilities/{abilities[i]}.png').resize((100, 100))
            template.paste(ability, (spells_cords[i]))
    else:
        normal_ability_counter = 0
        for i in range(4):
            if ability_list_reversed.get(abilities[i]) in ult_list:
                ult = abilities[i]
            else:
                ability = Image.open(f'./data/images/abilities/{abilities[i]}.png').resize((100, 100))
                template.paste(ability, (spells_cords[normal_ability_counter]))
                normal_ability_counter += 1
        ability = Image.open(f'./data/images/abilities/{ult}.png').resize((100, 100))
        template.paste(ability, ult_cords[0])
    return template

def drawtext(player, template, data):
    font = ImageFont.truetype(r'/home/artem/PycharmProjects/draftshare/draftshare/data/fonts/Inter-Italic.ttf', 32)
    networth = player['net_worth']
    kills, deaths, assists, lvl = player['kills'], player['deaths'], player['assists'], player['level']
    minute = data['result']['duration'] // 60
    text = f'{kills}/{deaths}/{assists} LV{lvl} NW{networth} {minute}M'
    needed = 479 #needed length of text in pixels so it can fit in the template
    sx, sy = 300, 129 #text start cords
    draw_text = ImageDraw.Draw(template)
    todraw = text.split()
    space_between = round((needed - draw_text.textlength(text, font=font)) / (len(todraw)-1)) #calculating needed space

    for i in todraw:
        if i != todraw[2]:
            draw_text.text((sx, sy), i, fill='#FFFFFF', font=font)
        else:
            draw_text.text((sx, sy), i, fill='#F5D85D', font=font)
        sx = sx + draw_text.textlength(i, font=font) + space_between


class MatchIdPlayerIdStatMin(APIView):
    def get(self, request, mid, pid):
        req = requests.get(f'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key={apikey}&match_id={mid}')
        data = json.loads(req.content)
        try:
            if data["result"]["error"]:
                return HttpResponse('Bad match id.')
            elif not data["result"]:
                return HttpResponse('SteamAPI is unavailable. Please try later.')
        except:
            pass

        for x in data["result"]["players"]:
            if pid == int(x["account_id"]):
                player = x
                break

        try:
            if player:
                pass
        except:
            return HttpResponse("Bad player id or User's match history is hidden.")

        abilities = getplayerattributes(player)
        template = drawimages(player, abilities, data)
        drawtext(player, template, data)

        response = HttpResponse(content_type='image/png')
        template.save(response, "PNG")
        return response

class MatchIdPlayerIdStat(APIView):
    def get(self, request, mid, pid, mode):
        print(mid, pid, mode)
        return HttpResponse(f'{mid}, {pid}, {mode}')

