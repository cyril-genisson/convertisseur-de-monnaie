#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Project: Forex Converter
# Filename: main.py
# Created: 27/11/2023
#
# Licence: GPLv3
#
# Author: Cyril GENISSON
#
import requests
import tradermade as tm
import pandas as pd


def header() -> None:
    string_menu_begin = "/" + "*" * 78 + "\\"
    string_menu_end = "\\" + "*" * 78 + "/"
    title = "FOREX CURRENCIES CHANGE"
    print(string_menu_begin)
    print(f"{title: ^80}")
    print(string_menu_end)
    print("\n")


def end() -> None:
    string_menu = "*" * 80
    print("\n")
    print(f"{string_menu}")
    print(f"{string_menu}")
    print("\n")


def menu() -> None:
    print("Option 1: Afficher le code ISO des monnaies")
    print("Option 2: Voir l'historique des transactions")
    print("Option 3: Effectuer une transaction de conversion")
    print("Option 4: Fin du programme")


def refresh_currencies_codes():
    tm.set_rest_api_key(APIKEY)
    tm.currency_list().to_csv("currencies.csv", mode="w", index=False)


def formatrequest(x: str, y: str) -> dict:
    request = {"from": x, "to": y, "api_key": APIKEY, "amount": 1000}
    return request


def conversion(devise1: str, devise2: str, value: float) -> None:
    querystring = formatrequest(devise1, devise2)
    response = requests.get(url, params=querystring)
    match str(response.status_code):
        case '200':
            conv = {'id': [response.json().get('timestamp')],
                    'from': [response.json().get('base_currency')],
                    'to': [response.json().get('quote_currency')],
                    'rate': [response.json().get('quote')],
                    'value': [val],
                    'convert': [round(value * response.json().get('quote'), 2)]}
            df = pd.DataFrame(conv)
            df.to_csv("history.csv", mode='a', index=False, header=False)
            print(df)
            print("Transaction réalisée avec succès:")
            print(f"{value} {devise1} -> {conv['convert'][0]} {devise2} au taux de change {conv['rate'][0]}")

        case '400':
            print(f"Erreur {response.status_code}: BAD REQUEST")
            print("Impossible d'effectuer le change.")

        case '401':
            print(f"Erreur {response.status_code}: API KEY INVALID")
            print("Impossible d'effectuer le change.")

        case '204':
            print(f"Erreur {response.status_code}: DATA NOT AVAILABLE")
            print("Impossible d'effectuer le change.")

        case '403':
            print(f"Erreur {response.status_code}: FORBIDDEN")
            print("Impossible d'effectuer le change.")


if __name__ == "__main__":
    url = "https://marketdata.tradermade.com/api/v1/convert"
    APIKEY = ""
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # à activer avec l'APIKEY rensignée pour mettre à jour le code des devises
    # refresh_currencies_codes()

    header()

    rep = 0
    while rep != '4':
        menu()
        rep = input("Veuillez entrer votre option: ")
        match rep:
            case '1':
                print("Code ISO des monnaies gérées")
                try:
                    df_currencies = pd.read_csv("currencies.csv", encoding="utf-8")
                    print(df_currencies)
                except:
                    print("Impossible d'ouvrir le fichier currencies.csv")
                finally:
                    end()

            case '2':
                print("Historique des transactions de change")
                try:
                    df_history = pd.read_csv("history.csv", encoding="utf-8")
                    print(df_history)
                except:
                    print("Impossible d'ouvrir le fichier history.csv")
                finally:
                    end()

            case '3':

                print("Nouvelle transaction de change:")
                dev1 = input("Code ISO de la monnaie de référence: ")
                dev2 = input("Code ISO de la monnaie de change: ")
                val = float(input("Valeur de la monnaie de référence à convertir: "))
                conversion(dev1, dev2, val)
                end()

            case '4':
                print("Fin du programme...")
                exit(0)

            case _:
                print("Option invalide")
                end()
