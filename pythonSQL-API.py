import sqlite3
import os
import sys

menu = '''
_____________________________________________________________________________
| typ k om een naam, achternaam, land en telefoon nummer toe te voegen.     |
| typ i om een naam, achternaam, land en telefoon nummer te verwijderen.    |
| typ p om een contact aan te passen.                                       |
| typ t om alle contacten en info te zien.                                  |
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
        print(gekozen_naam_verw + gekozen_achternaam_verw)
        c.execute("DELETE from Telefoonboek WHERE naam = :first AND achternaam = :last",
                    {'first': gekozen_naam_verw, 'last': gekozen_achternaam_verw})
        enter = input("Druk enter om verder te gaan. ")
    else:
        print("Dat is niet mogelijk. ")
        enter = input("Druk enter om het opnieuw te proberen. ")

    conn.commit()

def runner_code():
    doorgaan = True
    while doorgaan:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(menu)
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
        else:
            print("Dat is geen mogelijke keuze. ")
            enter = input("Druk enter om het opnieuw te proberen. ")

runner_code()
