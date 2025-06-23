import sqlite3
import random




conn = sqlite3.connect("ludzie.db")

cursor = conn.cursor()



nazwiska = [
    'Lis', 'Zawadzki', 'Sikora', 'Król', 'Baran', 'Górski', 'Tomaszewski', 'Wróbel', 'Pawlak', 'Walczak',
    'Michalak', 'Szulc', 'Kubiak', 'Bąk', 'Janik', 'Madej', 'Marciniak', 'Bednarek', 'Borowski', 'Bartosz',
    'Czerwiński', 'Urban', 'Piasecki', 'Wasilewski', 'Cieślak', 'Wysocki', 'Romanowski', 'Kopeć', 'Czajka', 'Jabłoński',
    'Nowacki', 'Tomczak', 'Gajda', 'Czech', 'Lipiński', 'Markowski', 'Sokołowski', 'Wieczorek', 'Kaczmarczyk', 'Olszewski',
    'Domański', 'Sobczak', 'Maj', 'Kaleta', 'Szewczyk', 'Bieniek', 'Trojanowski', 'Turek', 'Skowroński', 'Orłowski'
]



imiona = [
    'Aleksander', 'Szymon', 'Wojciech', 'Igor', 'Antoni', 'Emil', 'Franciszek', 'Karol', 'Mateusz', 'Hubert',
    'Jerzy', 'Zbigniew', 'Henryk', 'Daniel', 'Wiktor', 'Natalia', 'Zuzanna', 'Alicja', 'Anna', 'Maria',
    'Amelia', 'Helena', 'Klara', 'Nina', 'Magdalena', 'Martyna', 'Wiktoria', 'Ewa', 'Agata', 'Karolina',
    'Barbara', 'Iga', 'Milena', 'Hanna', 'Laura', 'Maja', 'Emilia', 'Joanna', 'Paulina', 'Gabriela',
    'Aniela', 'Blanka', 'Rozalia', 'Sara', 'Lena', 'Jagoda', 'Weronika', 'Julia', 'Aleksandra', 'Izabela'
]



mapa_kompanii = {
    1: 'Warszawa',
    2: 'Katowice',
    3: 'Szczecin',
    4: 'Białystok',
    5: 'Gdynia',
    6: 'Wrocław',
    7: 'Lublin',
    8: 'Poznań'
}


kompanie = list(range(1, 9))  # Kompanie jako liczby od 1 do 8
plutony = list(range(1, 6))   # Plutony jako liczby od 1 do 5



rekordy_ppor = []
rekordy_oficerowie = []
rekordy_podoficerowie = []



# 1. 40 x ppor., po 1 na pluton w każdej z 8 kompanii
for kompania in kompanie:
    lokalizacja = mapa_kompanii[kompania]
    for pluton in plutony:
        imie = random.choice(imiona)
        nazwisko = random.choice(nazwiska)

        rekordy_ppor.append((lokalizacja, kompania, pluton, "ppor.", imie, nazwisko))


# 2. Oficerowie – bez plutonu
uzyte_kompanie_oficerowie = set()
while len(rekordy_oficerowie) < 8:
    kompania = random.choice(kompanie)
    if kompania in uzyte_kompanie_oficerowie:
        continue
# for kompania in kompanie:
    lokalizacja = mapa_kompanii[kompania]
    stopien = random.choice(["por.", "kpt."])
    imie = random.choice(imiona)
    nazwisko = random.choice(nazwiska)
    rekordy_oficerowie.append((lokalizacja, kompania, None, stopien, imie, nazwisko))
    uzyte_kompanie_oficerowie.add(kompania)



# 3. Podoficerowie – bez plutonu
uzyte_kompanie_podoficerowie = set()
while len(rekordy_podoficerowie) < 8:
    kompania = random.choice(kompanie)
    if kompania in uzyte_kompanie_podoficerowie:
        continue
# for kompania in kompanie:
    lokalizacja = mapa_kompanii[kompania]
    stopien = random.choice(["kpr.", "plut.", "chor.", "st. chor."])
    imie = random.choice(imiona)
    nazwisko = random.choice(nazwiska)
    rekordy_podoficerowie.append((lokalizacja, kompania, None, stopien, imie, nazwisko))
    uzyte_kompanie_podoficerowie.add(kompania)




assert len(rekordy_ppor) == 40, f"Niepoprawna liczba ppor.: {len(rekordy_ppor)}"
assert len(rekordy_oficerowie) == 8 and len(set(r[1] for r in rekordy_oficerowie)) == 8, "Oficerowie nie są unikalni dla każdej kompanii!"
assert len(rekordy_podoficerowie) == 8 and len(set(r[1] for r in rekordy_podoficerowie)) == 8, "Podoficerowie nie są unikalni dla każdej kompanii!"

print("✔️  Dane przygotowane: 40 ppor., 8 oficerów (1/kompania), 8 podoficerów (1/kompania)")











wszystkie_rekordy = rekordy_ppor + rekordy_oficerowie + rekordy_podoficerowie

cursor.executemany("""
    INSERT INTO kadra (lokalizacja, kompania, pluton, "stopien", "imie", "nazwisko")
    VALUES (?, ?, ?, ?, ?, ?);
""", wszystkie_rekordy)

















#
# cursor.execute('\n'
#                '    CREATE TABLE IF NOT EXISTS kadra (\n'
#                '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
#                '        lokalizacja text not null ,\n'
#                '        kompania integer not null ,\n'
#                '        pluton integer \n'
#                '        \n'
#                '    )\n')
#
#
# try:
#     cursor.execute('alter table kadra  add column stopien text')
#     cursor.execute('ALTER TABLE kadra ADD COLUMN imie text')
#     cursor.execute('alter table kadra ADD COLUMN nazwisko text')
# except sqlite3.OperationalError:
#     print("Kolumna 'lokalizacja' już istnieje")


# rekordy = []
#
# for kompania in range(1, 9):  # 1 do 8
#     lokalizacja = mapa_kompanii[kompania]
#
#     for pluton in range(1, 6):  # pluton 1-5
#         imie = random.choice(imiona)
#         nazwisko = random.choice(nazwiska)
#         stopien = 'ppor.'
#         rekordy.append((lokalizacja, kompania, pluton, stopien, imie, nazwisko))
#pchorki
#     imie = random.choice(imiona)
#     nazwisko = random.choice(nazwiska)
#     stopien = random.choice(stopnie_dowodcy)
#     rekordy.append((lokalizacja, kompania, None, stopien, imie, nazwisko))
#
#     imie = random.choice(imiona)
#     nazwisko = random.choice(nazwiska)
#     stopien = random.choice(techniczni_stopnie)
#     rekordy.append((lokalizacja, kompania, None, stopien, imie, nazwisko, ))
#
#
#
#
#
#
#
# cursor.executemany("\n"
#                    "    INSERT INTO kadra (lokalizacja, kompania, pluton, \"stopien\", \"imie\", \"nazwisko\")\n"
#                    "    VALUES (?, ?, ?, ?, ?, ?)\n", rekordy)
#







conn.commit()
conn.close()


print("udało się")
