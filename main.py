import sqlite3

conn = sqlite3.connect("ludzie.db")


cursor = conn.cursor()

cursor.execute('\n'
               '    CREATE TABLE IF NOT EXISTS podchorazowie (\n'
               '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
               '        kompania integer NOT NULL,\n'
               '        pluton INTEGER NOT NULL\n'
               
               '        \n'
               '    )\n')

try:
    cursor.execute("ALTER TABLE podchorążowie ADD COLUMN imie TEXT")
    cursor.execute("ALTER TABLE podchorążowie ADD COLUMN nazwisko TEXT")

    print("Kolumny zostały dodane pomyślnie.")
except sqlite3.OperationalError as e:
    print(f"Błąd: {e}")





conn.commit()
conn.close()



