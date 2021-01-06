import sqlite3
import json
import collections
import psycopg2
import os
import sys
import requests
from pprint import pprint
#from flask import flask
y = {}
contact_mogelijkheden = {"Marijn"}
keuze_mogelijkheden = {"achternaam", "tel_nummer", "land"}
alles_menu = """
_____________________________________________________________________________
| typ f om een specifiek persoon te zoeken.                                 |
| typ k om alle personen en al hun info te zien.                            |
| typ q om terug te gaan naar het hoofd menu.                               |
|___________________________________________________________________________|
"""
API_menu = """
_____________________________________________________________________________
| typ k om alle info van de persoon te zien.                                |
| of maak een keuze uit de opties hieronder.                                |
| achternaam, tel_nummer of land.                                           |
|___________________________________________________________________________|
"""
menu = '''
_____________________________________________________________________________
| typ k om een naam, achternaam, land en telefoon nummer toe te voegen.     |
| typ i om een naam, achternaam, land en telefoon nummer te verwijderen.    |
| typ p om een contact aan te passen.                                       |
| typ t om alle contacten en info te zien.                                  |
| typ r om data uit de database te bekijken via de API.                     |
| typ q om het programma te sluiten.                                        |
|___________________________________________________________________________|
'''
conn = sqlite3.connect('Telefoonboek.db')
c = conn.cursor()
#c.execute("""CREATE TABLE Telefoonboek (
            #naam text,
            #achternaam text,
            #land,
            #tel_nummer int
            #)""")

def contact_toevoegen():
    os.system('cls' if os.name == 'nt' else 'clear')
    gekozen_naam = input("Wat is de naam van de persoon die je wilt toevoegen. ")
    gekozen_achternaam = input("Wat is de achternaam van de persoon die je wilt toevoegen. ")
    gekozen_land = input("Wat is het land van de persoon die je wilt toevoegen. ")
    gekozen_tel_nummer = input("Wat is het telefoon nummer van de persoon die je wilt toevoegen. ")
    in_Telefoonboek2 = c.execute("SELECT * FROM Telefoonboek WHERE naam = :first AND achternaam = :last",
                {'first': gekozen_naam, 'last': gekozen_achternaam}).fetchall()
    if in_Telefoonboek2:
        print("Dit contact bestaat al. ")
        enter = input("Druk enter om het opnieuw te proberen. ")
    else:
        c.execute("INSERT INTO Telefoonboek VALUES ('{}', '{}', '{}', {})".format(gekozen_naam, gekozen_achternaam, gekozen_land, gekozen_tel_nummer))
        conn.commit()
        enter = input("Druk enter om verder te gaan. ")

def contact_veranderen():
    gekozen_naam_ver = input("Wat is de naam van het contact. ")
    gekozen_achternaam_ver = input("Wat is de achternaam van het contact. ")
    in_Telefoonboek3 = c.execute("SELECT * FROM Telefoonboek WHERE naam = :first AND achternaam = :last",
                {'first': gekozen_naam_ver, 'last': gekozen_achternaam_ver}).fetchall()
    keuze = input("Wat wil je aanpassen van het contact het land of het tel_nummer. ")
    if keuze == "land":
        if in_Telefoonboek3:
            gekozen_land_ver = input("Wat is het nieuwe land van het contact. ")
            c.execute("UPDATE Telefoonboek SET land = :first2 WHERE naam = :first3 AND achternaam = :first4",
                        {'first2': gekozen_land_ver, 'first3': gekozen_naam_ver, 'first4': gekozen_achternaam_ver})
            conn.commit()
            enter = input("Druk enter om verder te gaan. ")
        else:
            print("Dat is niet mogelijk. ")
            enter = input("Druk enter om verder te gaan. ")
    elif keuze == "tel_nummer":
        if in_Telefoonboek3:
            gekozen_tel_nummer_ver = input("Wat is het nieuwe telefoon nummer van het contact. ")
            c.execute("UPDATE Telefoonboek SET tel_nummer = :first5 WHERE naam = :first6 AND achternaam = :first7",
                        {'first5': gekozen_tel_nummer_ver, 'first6': gekozen_naam_ver, 'first7': gekozen_achternaam_ver})
            conn.commit()
            enter = input("Druk enter om verder te gaan. ")
        else:
            print("Dat is niet mogelijk. ")
            enter = input("Druk enter om het opnieuw te proberen. ")
    else:
        print("Dat is niet mogelijk. ")
        enter = input("Druk enter om het opnieuw te proberen. ")

def contact_verwijderen():
    os.system('cls' if os.name == 'nt' else 'clear')
    gekozen_naam_verw = input("Wat is de naam van de persoon die je wilt verwijderen. ")
    gekozen_achternaam_verw = input("Wat is de achternaam het contact dat je wilt verwijderen. ")
    in_Telefoonboek = c.execute("SELECT * FROM Telefoonboek WHERE naam = :first AND achternaam = :last",
                {'first': gekozen_naam_verw, 'last': gekozen_achternaam_verw}).fetchall()
    if in_Telefoonboek:
        print(gekozen_naam_verw + " " + gekozen_achternaam_verw)
        c.execute("DELETE from Telefoonboek WHERE naam = :first AND achternaam = :last",
                    {'first': gekozen_naam_verw, 'last': gekozen_achternaam_verw})
        enter = input("Druk enter om verder te gaan. ")
    else:
        print("Dat is niet mogelijk. ")
        enter = input("Druk enter om het opnieuw te proberen. ")

    conn.commit()

#def maak_de_api():
    #c.execute("SELECT naam, achternaam, land ,tel_nummer FROM Telefoonboek")
    #rows = c.fetchall()
    #rowarray_list = []
    #y = {
        #"Marijn": [
            #{"achternaam": "Diepeveen"},
            #{"land": "Nederland"},
            #{"tel_nummer": "06666"}
        #]
        #}

    #for row in rows:
        ##t = (row[0], row[1], row[2], row[3])
        ##rowarray_list.append(t)
        #x = {
            #row[0]: [
                #{"achternaam": row[1]},
                #{"land": row[2]},
                #{"tel_nummer": row[3]}
            #]
            #}

        #y.update(x)

    ##j = json.dumps(rowarray_list)
    ##pprint(y)
    #de_API = json.dumps(y)
    ##rowarrays_file = 'Telefoonboek.json'
    #print(de_API)
    #return de_API

def maak_de_api2():
    conn_string = "host='localhost' dbname='Telefoonboek.db' user='me' password='pw'"
    conn = psycopg2.connect(conn_string)
    c.execute("SELECT * FROM Telefoonboek")
    rows = cursor.fetchall()
    rowarray_list = []

    for row in rows:
        t = (row[0], row[1], row[2], row[3])
        rowarray_list.append(t)

    j = json.dumps(rowarray_list)

    with open("student_rowarrays.js", "w") as f:
        f.write(j)
        objects_list = []

    for row in rows:
        d = collections.OrderedDict()
        d["naam"] = row[0]
        d["achternaam"] = row[1]
        d["land"] = row[2]
        d["tel_nummer"] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)

    with open("student_objects.js", "w") as f:
        f.write(j)
    conn.close()
    pprint(j)

def runner_code():
    doorgaan = True
    while doorgaan:
        c.execute("SELECT naam, achternaam, land ,tel_nummer FROM Telefoonboek")
        rows = c.fetchall()
        rowarray_list = []
        for row in rows:
            #t = (row[0], row[1], row[2], row[3])
            #rowarray_list.append(t)
            x = {
                row[0]: {
                    'achternaam': row[1],
                    'land': row[2],
                    'tel_nummer': row[3]}
                }

            xz = {row[0]}
            contact_mogelijkheden.update(xz)

            y.update(x)
            #de_API2 = requests.get(y)

        with open("Telefoonboek.json", "w") as write_file:
            json.dump(y, write_file)
        #response = requests.get(, "Telefoonboek.json")
        #de_API = flask.jsonify(y)
        #de_API = json.dumps(y)
        #de_API = json.loads(y)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(menu)
        #print(xy)
        #de_API2 = de_API.json()
        #print(y)
        keuze_gebruiker = input("Wat is je keuze uit het bovenstaande menu. ")
        if keuze_gebruiker == "k":
            contact_toevoegen()
        elif keuze_gebruiker == "i":
            contact_verwijderen()
        elif keuze_gebruiker == "p":
            contact_veranderen()
        elif keuze_gebruiker == "t":
            c.execute("SELECT * FROM Telefoonboek")
            print(c.fetchall())
            enter = input("Druk enter om door te gaan. ")
        elif keuze_gebruiker == "q":
            doorgaan = False
        elif keuze_gebruiker == "r":
            #pprint(response)
            print(alles_menu)
            alles_zien = input("Maak een keuze uit het bovenstaande menu. ")
            if alles_zien == "f":
                naam_keuze = input("Wat is de naam van de persoon die je wilt bekijken. ")
                if naam_keuze in contact_mogelijkheden:
                    print(API_menu)
                    optie_gebruiker = input("Wat is je keuze uit het menu hierboven? ")
                    if optie_gebruiker == "k":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(naam_keuze + " " + y[naam_keuze]["achternaam"])
                        print(naam_keuze + " woont in " + y[naam_keuze]["land"])
                        print(y[naam_keuze]["tel_nummer"])
                        enter = input("Druk enter om door te gaan. ")
                    if optie_gebruiker == "achternaam":
                        print(y[naam_keuze][optie_gebruiker])
                        enter = input("Druk enter om door te gaan. ")
                    if optie_gebruiker == "tel_nummer":
                        print(y[naam_keuze][optie_gebruiker])
                        enter = input("Druk enter om door te gaan. ")
                    if optie_gebruiker == "land":
                        print(y[naam_keuze][optie_gebruiker])
                        enter = input("Druk enter om door te gaan. ")
                    else:
                        print("Dat is niet mogelijk. ")
                        enter = input("Druk enter om door te gaan. ")
                else:
                    print("Dat persoon staat niet in het telefoonboek. ")
                    enter = input("Druk enter om door te gaan. ")
            elif alles_zien == "k":
                pprint(y)
                enter = input("Druk enter om door te gaan. ")
            else:
                enter = input("Druk enter om het opnieuw te proberen. ")
        else:
            print("Dat is geen mogelijke keuze. ")
            enter = input("Druk enter om het opnieuw te proberen. ")

runner_code()
