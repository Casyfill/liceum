import requests
from bs4 import BeautifulSoup
from random import choice
import warnings
import os
import json


warnings.filterwarnings("ignore")


urls_by_categories = {
    'Fruits': 'https://www.enchantedlearning.com/wordlist/fruit.shtml',
    'Colors': 'https://www.enchantedlearning.com/wordlist/colors.shtml',
    'Plants': 'https://www.enchantedlearning.com/wordlist/plants.shtml',
    'Sport': 'https://www.enchantedlearning.com/wordlist/sports.shtml',
    # 'Elements': 'https://www.enchantedlearning.com/wordlist/elements.shtml',
    'Vegetables': 'https://www.enchantedlearning.com/wordlist/vegetables.shtml',
    # 'Trees': 'https://www.enchantedlearning.com/wordlist/trees.shtml',
}


def get_categories():
    return urls_by_categories.keys()


def get_word(category):
    if not os.path.isfile('data.json'):
        with open('data.json', 'w') as f:
            json.dump({key: [] for key in urls_by_categories.keys()}, f)

    with open('data.json', 'r') as f:
        data = json.load(f)

    if len(data[category]) != 0:
        return choice(data[category])

    resp = requests.get(urls_by_categories[category])
    parse1 = BeautifulSoup(resp.text)
    words = []
    for parse2 in parse1.find_all('div', {'class': 'wordlist-item'}):
        if parse2.contents[0].find(' ') == -1:
            words.append(parse2.contents[0])
    data[category] = words

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return choice(words)
