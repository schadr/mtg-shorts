import requests
import bz2
import json
from enum import Enum

card_info_api_endpoint = 'https://mtgjson.com/api/v5/'
price_file_name = 'AllPricesToday.json.bz2'

price_cache = {}
card_cache = {}

class Type(Enum):
    NORMAL = "normal"
    FOIL = "foil"

class Card:
    def __init__(self, uuid, name, number, mtg_set):
        self.uuid = uuid
        self.name = name
        self.number = number
        self.mtg_set = mtg_set
        self.price = -1.0
        self.price_foil = -1.0
        if uuid in price_cache:
            self.price = price_cache[uuid]['normal']
            self.price_foil = price_cache[uuid]['foil']
    
    def __str__(self):
        return "uuid: " + self.uuid + ", name: \"" + self.name + "\", set: " + self.mtg_set + ", number: " + str(self.number) + ", price: " + str(self.price) + ", price foil: " + str(self.price_foil)

def load_card_cache(mtg_set):
    if len(price_cache) == 0:
        price_request = requests.get(card_info_api_endpoint + price_file_name)
        price_json = json.loads(bz2.decompress(price_request.content).decode('utf-8'))
        price_date = price_json["meta"]["date"]
        for price_entry_key in price_json['data'].keys():
            price_cache[price_entry_key] = {}
            price_cache[price_entry_key]['normal'] = -1.0
            price_cache[price_entry_key]['foil'] = -1.0
            if 'paper' in price_json['data'][price_entry_key] and 'tcgplayer' in price_json['data'][price_entry_key]['paper']:
                retail = price_json['data'][price_entry_key]['paper']['tcgplayer']['retail']
                if 'normal' in retail:
                    price_cache[price_entry_key]['normal'] = retail['normal'][price_date]
                if 'foil' in retail:
                    price_cache[price_entry_key]['foil'] = retail['foil'][price_date]
                pass

    if mtg_set in card_cache:
        pass
    card_cache[mtg_set] = {}
    card_info_request = requests.get(card_info_api_endpoint + mtg_set +'.json')
    for card in card_info_request.json()['data']['cards']:
        uuid = card['uuid']
        name = card['name']
        number = card['number']
        if number.isdecimal():
            card_cache[mtg_set][int(number)] = Card(uuid, name, int(number), mtg_set)
        #pass
    
def get_price(mtg_set, card_number, type = Type.NORMAL):
    load_card_cache(mtg_set)
    print(card_cache[mtg_set][card_number])
    if type == Type.NORMAL:
        return card_cache[mtg_set][card_number].price
    return card_cache[mtg_set][card_number].price_foil

def get_card(mtg_set, card_number):
    load_card_cache(mtg_set)
    if card_number in card_cache[mtg_set]:
        return card_cache[mtg_set][card_number]
    return None

def convert_to_cards(set_card_numbers):
    cards = []
    for frame in set_card_numbers:
        if frame == ():
            cards.append(None)
        else:
            mtg_set = frame[0]
            card_number = frame[1]
            cards.append(get_card(mtg_set, card_number))
    return cards