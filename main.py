import sqlite3
import random


imiona = [
    'Jan', 'Piotr', 'Tomasz', 'Marek', 'Paweł', 'Andrzej', 'Krzysztof', 'Adam', 'Michał', 'Grzegorz',
    'Łukasz', 'Marcin', 'Sebastian', 'Rafał', 'Kamil', 'Oliwia', 'Kamila', 'Julka', 'Patrycja', 'Filip', 'Bartosz', 'Jakub', 'Dominika'
]

nazwiska = [
    'Kowalski', 'Nowak', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński',
    'Szymański', 'Woźniak', 'Dąbrowski', 'Kozłowski', 'Jankowski', 'Mazur', 'Krawczyk', 'Krakowiak', 'Stępa', 'Łuda'
]

miasta = [
    'Warszawa', 'Poznań', 'Katowice', 'Białystok', 'Radom', 'Gdańsk', 'Gdynia', 'Szczecin', 'Toruń', 'Kraków', 'Zielona Góra', 'Łódź', 'Wrocław', 'Bydgoszcz', 'Lublin', 'Częstochowa', 'Sosnowiec', 'Kielce', 'Rzeszów', 'Gliwice', 'Zabrze', 'Olsztyn', 'Bytom', 'Rybnik', 'Augustów', 'Opole', 'Płock', 'Koszalin', 'Kalisz'
]

conn = sqlite3.connect("ludzie.db")

cursor = conn.cursor()

cursor.execute('\n'
               '    CREATE TABLE IF NOT EXISTS podchorazowie (\n'
               '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
               '        kompania integer NOT NULL,\n'
               '        pluton INTEGER NOT NULL\n'
               
               '        \n'
               '    )\n')





rekordy = []
for _ in range(1000):
    imie = random.choice(imiona)
    nazwisko = random.choice(nazwiska)
    kompania = random.randint(1, 8)
    pluton = random.randint(1, 5)
    lokalizacja = random.choice(miasta)
    rekordy.append((kompania, pluton, imie, nazwisko, lokalizacja))

cursor.executemany("""
    INSERT INTO podchorążowie (kompania, pluton, "imie", "nazwisko", "lokalizacja")
    VALUES (?, ?, ?, ?, ?)
""", rekordy)




conn.commit()
conn.close()



