# -*- coding: utf-8 -*-
import json
import random
import pprint
import os
from pyfiglet import Figlet

with open('food_list.json') as file:
    food_list = json.load(file)


def add_dish():
    # {"name": "Käse", "id": 31, "schlagworte": ""}
    dic = {"name": "", "id": 0, "schlagworte": ""}
    name = input("Wie ist der Name des hinzuzufügenden Gerichts?\n")
    schlagworte = input("Was sind die zugehörigen Schlagworte?\n")
    dic["name"] = name
    dic["id"] = len(food_list['Gerichte']) + 1
    dic["schlagworte"] = schlagworte
    food_list['Gerichte'].append(dic)
    with open('food_list.json', 'w') as f:
        json.dump(food_list, f, ensure_ascii=False, indent=4)
    ant = input("Willst du ein weiteres Gericht hinzufügen? [Y/N]\n")
    if ant == 'Y' or ant == 'y':
        add_dish()
    else:
        print("Ok, tschau")


def random_dish():
    end = len(food_list['Gerichte']) 
    no = random.randrange(1, end)
    for i in range(0, end):
        food_id = food_list['Gerichte'][i]['id']
        if food_id == no:
            answer = input("Wie wärs mit " + food_list['Gerichte'][i]['name'] + " zum Abendbrot?")
            if answer != 'cool':
                random_dish()
            else:
                print("Super, guten Appetit!")

    return food_list['Gerichte'][i]['name']


def schlagworte_register():
    s = []
    length = len(food_list['Gerichte'])
    for j in range(0, length):
        food_schlagworte = food_list['Gerichte'][j]['schlagworte'].split(", ")
        s = s + food_schlagworte
    schlagworte = list(set(s))
    print("Das sind mögliche Schlagworte:")
    pprint.pprint(sorted(schlagworte))


def erweiterte_suche(param):
    parameter = param.split(' ')
    pos_dishes = []
    length = len(food_list['Gerichte'])
    for l in range(0, length):
        for p in parameter:
            if p in food_list['Gerichte'][l]['schlagworte'].lower():
                pos_dishes.append(food_list['Gerichte'][l]['id'])
    ran = random.choice(pos_dishes)
    for r in range(0, length):
        food_id = food_list['Gerichte'][r]['id']
        if food_id == ran:
            answer = input("Wie wärs mit " + food_list['Gerichte'][r]['name'] + " zum Abendbrot?")
            if answer != 'cool':
                erweiterte_suche(param)
            else:
                print("Super, guten Appetit!")


def get():
    ant2 = input("Willst du nur Gerichte mit bestimmten Schlagworten vorgeschlagen bekommen? [Y/N]\n")
    if ant2 == 'N' or ant2 == 'n':
        random_dish()
    elif ant2 == 'Y' or ant2 == 'y':
        schlagworte_register()
        param = input("Nach welchen Schlagworten möchtest du suchen?\n")
        erweiterte_suche(param.lower())
    else:
        print("Das war leider keine gültige Antwort, versuchen wirs nochmal!")
        get()

colors = {
    'c': '\033[36m',
    'y': '\033[33m',
    'b': '\033[34m',
}

def colorize(string, color):

    if color not in colors:
        return string
    return colors[color] + string + '\033[37m'

def frage():
    ant1 = input("Willst du etwas zur DB hinzufügen oder etwas vorgeschlagen bekommen?\n(1) Add\n(2) Get\n")
    if ant1.lower() == "get" or ant1 == "2":
        get()
    elif ant1.lower() == 'add' or ant1 == "1":
        add_dish()
    else:
        print("Das war leider keine gültige Antwort, versuchen wirs nochmal!")
        frage()

def main():
    os.system('clear')
    f = Figlet(font='banner')
    print(colorize(str(f.renderText('Food')), 'y'))
    print(colorize(str(f.renderText('Planner')), 'y'))
    frage()

main()