# -*- coding: utf-8 -*-
import json
import os
import pprint
import random
from difflib import SequenceMatcher
from os.path import exists

from pyfiglet import Figlet


def add_dish(food_dict: dict, food_names: list):
    # {"name": "Käse", "id": 31, "schlagworte": ""}
    dic = {"name": "", "id": 0, "schlagworte": []}
    name = input("Wie ist der Name des hinzuzufügenden Gerichts?\n")
    if name.lower() == "exit":
        return ()
    dic["name"] = name
    similar_dishes = get_similar_dishes(food_names, name)
    if len(similar_dishes) != 0:
        print(
            f"Es gibt mindestens ein Gericht mit einem ähnlichen Namen in deiner Datenbank. \nÄhnliche Gerichte:"
        )
        for dish in similar_dishes:
            print(f'\t {colorize("•", "c")} {dish}')
        ant = input("Ist das Gericht, welches du gerade hinzufügen wolltest dabei? [J/N]")
        if ant.lower() == "exit":
            return ()
        if ant.lower() == "j":
            print(
                "Alles klar, dann ignorier ich deine Anfrage zum Hinzufügen eines neuen Gerichts!"
            )
            add_one_more_dish(food_dict, food_names)
            return ()
    dic["id"] = len(food_dict["Gerichte"]) + 1
    schlagworte = [x.strip() for x in input("Was sind die zugehörigen Schlagworte?\n").split(",")]
    if "exit" in schlagworte:
        return ()
    dic["schlagworte"] = schlagworte
    food_dict["Gerichte"].append(dic)
    with open("food_dict.json", "w+") as file:
        json.dump(food_dict, file, ensure_ascii=False, indent=4)
    add_one_more_dish(food_dict, food_names)


def add_one_more_dish(food_dict: dict, food_names: list):
    ant = input("Willst du ein weiteres Gericht hinzufügen? [J/N]\n")
    if ant.lower() == "exit":
        return ()
    if ant.lower() == "j":
        add_dish(food_dict, food_names)
    else:
        print("Ok, tschau")


def get_similar_dishes(food_names: list, name: str) -> list:
    similar_dishes = []
    for n in food_names:
        similarity = similar(n, name)
        if similarity >= 0.3:
            similar_dishes.append(n)

    return similar_dishes


def get_random_dish(food_dict: dict, food_names: list):
    end = len(food_dict["Gerichte"])
    answer = input(f"Wie wärs mit {random.choice(food_names)} zum Abendbrot?")
    if answer.lower() == "exit":
        return ()
    if answer != "cool":
        get_random_dish(food_dict, food_names)
    else:
        print("Super, guten Appetit!")


def schlagworte_register(food_dict: dict) -> None:
    s = []
    length = len(food_dict["Gerichte"])
    for j in range(0, length):
        food_schlagworte = food_dict["Gerichte"][j]["schlagworte"]
        s += food_schlagworte
    food_schlagworte = list(set(s))
    print("Das sind mögliche Schlagworte:")
    pprint.pprint(sorted(food_schlagworte))


def erweiterte_suche(food_dict: dict, param):
    parameter = param.split(" ")
    pos_dishes = []
    length = len(food_dict["Gerichte"])
    for l in range(0, length):
        for p in parameter:
            if p in [x.lower() for x in food_dict["Gerichte"][l]["schlagworte"]]:
                pos_dishes.append(food_dict["Gerichte"][l]["id"])
    ran = random.choice(pos_dishes)
    answer = input("Wie wärs mit " + food_dict["Gerichte"][ran - 1]["name"] + " zum Abendbrot?")
    if answer.lower() == "exit":
        return ()
    if answer != "cool":
        erweiterte_suche(food_dict, param)
    else:
        print("Super, guten Appetit!")


def get(food_dict: dict, food_names: list):
    """_summary_

    Args:
        food_dict (dict): _description_
        food_names (list): _description_
    """
    ant2 = input(
        "Willst du nur Gerichte mit bestimmten Schlagworten vorgeschlagen bekommen? [J/N]\n"
    )
    if ant2.lower() == "exit":
        return ()
    if ant2.lower() == "n":
        get_random_dish(food_dict, food_names)
    elif ant2.lower() == "j":
        schlagworte_register(food_dict)
        param = input("Nach welchen Schlagworten möchtest du suchen?\n")
        if param.lower() == "exit":
            return ()
        erweiterte_suche(food_dict, param.lower())
    else:
        print("Das war leider keine gültige Antwort, versuchen wirs nochmal!")
        get(food_dict, food_names)


def frage(food_dict: dict, food_names: list):
    """Ask question.

    Args:
        food_dict (dict): food dictionary
        food_names (list): list of food names
    """
    ant1 = input(
        "Willst du etwas zu deiner Essensdatenbank hinzufügen oder etwas vorgeschlagen bekommen?\n(1) Hinzufügen \n(2) Vorschlag \n(3) EXIT, bitte lass mich raus!\n"
    )
    if ant1.lower() == "get" or ant1 == "2":
        if len(food_names) == 0:
            print(
                "Upsi, scheinbar hast du noch gar keine Gerichte in deiner Datenbank. Füge schnell welche hinzu!"
            )
            ant2 = input(
                "Willst du jetzt direkt ein Gericht zu deiner Datenbank hinzufügen? [J/N]\n"
            )
            if ant2.lower() == "j":
                add_dish(food_dict, food_names)
            print(f"Na gut, {random.choice(liste_witziger_verabschiedungen)}!")
        else:
            get(food_dict, food_names)
    elif ant1.lower() == "add" or ant1 == "1":
        add_dish(food_dict, food_names)
    elif ant1.lower() == "exit" or ant1 == "3":
        print(colorize(f"{random.choice(liste_witziger_verabschiedungen)}!", "c"))
        return ()
    else:
        print("Das war leider keine gültige Antwort, versuchen wirs nochmal!")
        frage(food_dict, food_names)


# Hilfsfunktionen
def create_list_of_food_names(food_dict: dict) -> list:
    """Create a list of all the food names from the dictionary for get_random_dish.

    Args:
        food_dict (dict): dictionary with all foods

    Returns:
        food_names: list of all food names
    """
    food_names = []
    for food in food_dict["Gerichte"]:
        food_names.append(food["name"])
    return food_names


def similar(a: str, b: str) -> int:
    return SequenceMatcher(None, a, b).ratio()


colors = {
    "c": "\033[36m",
    "y": "\033[33m",
    "b": "\033[34m",
}


def colorize(string, color):
    if color not in colors:
        return string
    return colors[color] + string + "\033[37m"


def main():
    os.system("clear")
    try:
        with open("pyfigletfonts.txt") as f:
            fonts = f.read().splitlines()
        font = random.choice(fonts)
    except FileNotFoundError:
        font = "univers"
    figlet = Figlet(font=font, width=800)
    if exists("food_dict.json"):
        with open("food_dict.json", "r") as file:
            food_dict = json.load(file)
    else:
        food_dict = {"Gerichte": []}
    print(
        f'{colorize(str(figlet.renderText("FOOD")), "y")}'
        + r"""                   _..----.._       
                 .'     o    '.     
                /   o       o  \   
               |o        o     o|   
               /'-.._o     __.-'\  
               \      `````     /   
               |``--........--'`|    
                \              /
                 `'----------'`
"""
    )
    print(f'{colorize(str(figlet.renderText("PLANNER")), "c")}')
    food_names = create_list_of_food_names(food_dict)
    frage(food_dict, food_names)


liste_witziger_verabschiedungen = [
    # "Tschausenberger",
    "Ciao Kakao",
    # "Tschö mit ö",
    # "Tschüssikowski",
    # "Arrivischerzi",
    "Bis Baldrian",
    # "Bis denne, Antenne",
    "Bis spätersilie",
    "Bye Bye, Kartoffelbrei",
    "Byesilikum",
    # "Machs gut, Knut",
    # "San Frantschüssko",
    "Sayonara, Carbonara",
    "Tschüsli Müsli",
    "Wirsing, man sieht sich",
]

try:
    main()
except KeyboardInterrupt:
    print(f"\nOk, dann nicht, {random.choice(liste_witziger_verabschiedungen)}")
