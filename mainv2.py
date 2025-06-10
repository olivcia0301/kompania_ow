import sqlite3
import random




conn = sqlite3.connect("ludzie.db")

cursor = conn.cursor()

# imiona = [
#     'Jan', 'Piotr', 'Tomasz', 'Marek', 'Paweł', 'Andrzej', 'Krzysztof', 'Adam', 'Michał', 'Grzegorz',
#     'Łukasz', 'Marcin', 'Sebastian', 'Rafał', 'Kamil', 'Oliwia', 'Kamila', 'Julka', 'Patrycja', 'Filip', 'Bartosz',
#     'Jakub', 'Dominika'
# ]
#
#
#
# nazwiska = [
#     'Kowalski', 'Nowak', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński',
#     'Szymański', 'Woźniak', 'Dąbrowski', 'Kozłowski', 'Jankowski', 'Mazur', 'Krawczyk', 'Krakowiak', 'Stępa', 'Łuda'
# ]



# mapa_kompanii = {
#     1: 'Warszawa',
#     2: 'Katowice',
#     3: 'Szczecin',
#     4: 'Białystok',
#     5: 'Gdynia',
#     6: 'Wrocław',
#     7: 'Lublin',
#     8: 'Poznań'
# }


cursor.execute('\n'
               '    CREATE TABLE IF NOT EXISTS kadra (\n'
               '        lokalizacja text not null,\n'
               '        kompania integer not null ,\n'
               '        stopien integer NOT NULL\n'
               '        \n'
               '    )\n')


# rekordy = []
# for _ in range(25):
#     imie = random.choice(imiona)
#     nazwisko = random.choice(nazwiska)
#     kompania = random.randint(1, 8)
#     pluton = random.randint(1, 5)
#     lokalizacja = mapa_kompanii[kompania]
#     rekordy.append((lokalizacja, kompania, pluton, imie, nazwisko))
#
# cursor.executemany('\n'
#                    '    INSERT INTO pchorki (lokalizacja, kompania, \"pluton\", \"imie\", \"nazwisko\")\n'
#                    '    VALUES (?, ?, ?, ?, ?)\n', rekordy)
# print("Dodano 150 losowych podchorążych do bazy danych.")



conn.commit()
conn.close()


print("udało się")
