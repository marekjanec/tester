# Tester3000

Pointa je, že máš jeden .py súbor ten len spustíš a môžeš sa učiť otázky a odpovede z .csv súboru s 2 stĺpacami "otazka"
a "odpoved". Má to svoje :bug: bugy :bug:, nie jo to na 100% blbuvzdorné. Prispievanie otázkami alebo upgradami je vítané.

## Funkcie

* Načítanie .csv s otazkami a odpovedami

otazka | odpoved |
--- | --- |
... | ... |

* Uloženie / načítanie .json súboru s aktálnym stavom testera
* Vytvorenie prázdneho .csv suboru
* Pridanie/aktualizovanie/vymazanie otazky
* Reštart tester
  * nanovo načita otazky a resetne hodnoty
* Vyčistenie textových polí
* V menu
  * Vytvorenie simuliacie skúšku
    * výber súboru s otázkami
    * výber počtu náhodných otázok do skúšky
    * počítanie správnych /nesprávnych odpovedí

## Kód na kokód

Python 3.8

## Importy knižníc
* csv
* json
* random
* tkinter
* types