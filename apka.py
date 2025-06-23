import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests
from bs4 import BeautifulSoup
from tkintermapview import TkinterMapView

DB = 'ludzie.db'

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

def connect_db():
    return sqlite3.connect(DB)

def get_coordinates(location):
    try:
        address_url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(address_url).text
        soup = BeautifulSoup(response, "html.parser")
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except Exception:
        return None

bg_color = "#2e2e2e"
fg_color = "#d3d3d3"
entry_bg = "#3c3f41"
btn_bg = "#444444"
btn_fg = fg_color
highlight_color = "#ffb6c1"

okno = tk.Tk()
okno.title("Zarządzanie kompaniami")
okno.configure(bg=bg_color)

frame_buttons = tk.Frame(okno, bg=bg_color)
frame_buttons.pack(pady=10)

frame_controls = tk.Frame(okno, bg=bg_color)
frame_controls.pack()

frame_table = tk.Frame(okno, bg=bg_color)
frame_table.pack()

frame_map = tk.Frame(okno)
frame_map.pack()

map_widget = TkinterMapView(frame_map, width=800, height=400)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)
map_widget.pack()

current_table = None
tree = None
entry_filter_kompania = None
entry_filter_pluton = None

def ustaw_styl_drzewa(tree_widget):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
                    background=bg_color,
                    foreground=fg_color,
                    fieldbackground=bg_color,
                    font=('Segoe UI', 10))
    style.map('Treeview', background=[('selected', highlight_color)],
              foreground=[('selected', 'black')])
    tree_widget.tag_configure('oddrow', background="#3c3f41")
    tree_widget.tag_configure('evenrow', background="#2e2e2e")


def pokaz_kompanie():
    map_widget.delete_all_marker()
    for nr, miejscowosc in mapa_kompanii.items():
        wsp = get_coordinates(miejscowosc)
        if wsp:
            map_widget.set_marker(
                wsp[0], wsp[1],
                text=f"Kompania {nr}",
                marker_color_circle="#00BFFF",
                marker_color_outside="#00BFFF"
            )







def pokaz_tabele(table_name):
    global current_table, tree, entry_filter_kompania, entry_filter_pluton
    current_table = table_name

    for widget in frame_controls.winfo_children():
        widget.destroy()
    for widget in frame_table.winfo_children():
        widget.destroy()
    map_widget.delete_all_marker()

    tk.Label(frame_controls, text="Kompania:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=5, pady=2)
    entry_filter_kompania = tk.Entry(frame_controls, width=5, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    entry_filter_kompania.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_controls, text="Pluton:", bg=bg_color, fg=fg_color).grid(row=0, column=2, padx=5, pady=2)
    entry_filter_pluton = tk.Entry(frame_controls, width=5, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    entry_filter_pluton.grid(row=0, column=3, padx=5, pady=2)

    buttons = [
        ("Filtruj", odswiez),
        ("Odśwież", odswiez),
        ("Edytuj", edytuj),
        ("Usuń", usun),
        ("Dodaj", dodaj),
        ("Pokaż szczegóły", pokaz_szczegoly),
        ("Pokaż kompanie", pokaz_kompanie),
    ]
    for i, (txt, cmd) in enumerate(buttons):
        tk.Button(frame_controls, text=txt, command=cmd, bg=btn_bg, fg=btn_fg, activebackground=highlight_color).grid(
            row=0, column=4 + i, padx=3, pady=2)


    if current_table == "kadra":
        kolumny = ("id", "lokalizacja", "kompania", "pluton", "stopien", "imie", "nazwisko")
    else:
        kolumny = ("id", "kompania", "lokalizacja", "pluton", "imie", "nazwisko")

    tree = ttk.Treeview(frame_table, columns=kolumny, show='headings', height=15)
    for col in kolumny:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=110, anchor="center")
    tree.pack()

    ustaw_styl_drzewa(tree)

    odswiez()

def odswiez():
    for item in tree.get_children():
        tree.delete(item)
    map_widget.delete_all_marker()

    komp = entry_filter_kompania.get()
    plut = entry_filter_pluton.get()

    query = f"SELECT * FROM {current_table} WHERE 1=1"
    params = []

    if komp:
        query += " AND kompania = ?"
        params.append(int(komp))
    if plut:
        query += " AND pluton = ?"
        params.append(int(plut))

    conn = connect_db()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    kolumny = tree["columns"]
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        row_dict = dict(zip(kolumny, row))
        tree.insert('', 'end', values=[row_dict[k] for k in kolumny], tags=(tag,))

def dodaj_marker_na_mapie(miejsce):
    wsp = get_coordinates(miejsce)
    if wsp:
        map_widget.set_marker(wsp[0], wsp[1], text="⭐", marker_color_circle=highlight_color, marker_color_outside=highlight_color)

def pokaz_szczegoly():
    wybrany = tree.focus()
    if not wybrany:
        messagebox.showinfo("Info", "Zaznacz rekord.")
        return
    values = tree.item(wybrany)['values']
    kolumny = tree["columns"]
    rekord = dict(zip(kolumny, values))

    map_widget.delete_all_marker()
    lokalizacja = rekord["lokalizacja"]
    wsp = get_coordinates(lokalizacja)
    if wsp:
        map_widget.set_position(*wsp)
        map_widget.set_zoom(17)
        map_widget.set_marker(wsp[0], wsp[1], text="⭐", marker_color_circle=highlight_color, marker_color_outside=highlight_color)



def edytuj():
    wybrany = tree.focus()
    if not wybrany:
        messagebox.showwarning("Błąd", "Zaznacz rekord.")
        return
    values = tree.item(wybrany)['values']
    kolumny = tree["columns"]
    rekord = dict(zip(kolumny, values))
    id_rekordu = rekord["id"]

    nowe_okno = tk.Toplevel(okno)
    nowe_okno.title("Edycja")
    nowe_okno.configure(bg=bg_color)

    if current_table == "kadra":
        labels = ["kompania", "pluton", "stopien", "imie", "nazwisko"]
        dane_start = [rekord["kompania"], rekord["pluton"], rekord["stopien"], rekord["imie"], rekord["nazwisko"]]
    else:
        labels = ["kompania", "pluton", "imie", "nazwisko"]
        dane_start = [rekord["kompania"], rekord["pluton"], rekord["imie"], rekord["nazwisko"]]

    entries = []
    for i, label in enumerate(labels):
        tk.Label(nowe_okno, text=label.capitalize(), bg=bg_color, fg=fg_color).grid(row=i, column=0, padx=5, pady=3, sticky='w')
        e = tk.Entry(nowe_okno, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
        e.insert(0, dane_start[i])
        e.grid(row=i, column=1, padx=5, pady=3)
        entries.append(e)

    def zapisz():
        dane = [e.get() for e in entries]
        try:
            komp_int = int(dane[0])
            lokalizacja = mapa_kompanii.get(komp_int, "Nieznana")
        except Exception:
            messagebox.showerror("Błąd", "Kompania musi być liczbą od 1 do 8")
            return

        conn = connect_db()
        c = conn.cursor()
        if current_table == "kadra":
            c.execute("UPDATE kadra SET kompania=?, lokalizacja=?, pluton=?, stopien=?, imie=?, nazwisko=? WHERE id=?",
                      (komp_int, lokalizacja, dane[1], dane[2], dane[3], dane[4], id_rekordu))
        else:
            c.execute("UPDATE pchorki SET kompania=?, lokalizacja=?, pluton=?, imie=?, nazwisko=? WHERE id=?",
                      (komp_int, lokalizacja, dane[1], dane[2], dane[3], id_rekordu))
        conn.commit()
        conn.close()
        nowe_okno.destroy()
        odswiez()

    tk.Button(nowe_okno, text="Zapisz", command=zapisz, bg=btn_bg, fg=btn_fg, activebackground=highlight_color).grid(row=len(labels), column=0, columnspan=2, pady=10)

def usun():
    wybrany = tree.focus()
    if not wybrany:
        messagebox.showwarning("Błąd", "Zaznacz rekord.")
        return
    values = tree.item(wybrany)['values']
    id_rekordu = values[0]
    if messagebox.askyesno("Potwierdzenie", "Usunąć rekord?"):
        conn = connect_db()
        c = conn.cursor()
        c.execute(f"DELETE FROM {current_table} WHERE id=?", (id_rekordu,))
        conn.commit()
        conn.close()
        odswiez()

def dodaj():
    nowe_okno = tk.Toplevel(okno)
    nowe_okno.title("Dodaj rekord")
    nowe_okno.configure(bg=bg_color)

    if current_table == "kadra":
        labels = ["kompania", "pluton", "stopien", "imie", "nazwisko"]
    else:
        labels = ["kompania", "pluton", "imie", "nazwisko"]

    entries = []
    for i, label in enumerate(labels):
        tk.Label(nowe_okno, text=label.capitalize(), bg=bg_color, fg=fg_color).grid(row=i, column=0, padx=5, pady=3, sticky='w')
        e = tk.Entry(nowe_okno, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
        e.grid(row=i, column=1, padx=5, pady=3)
        entries.append(e)

    def zapisz():
        dane = [e.get() for e in entries]
        try:
            komp_int = int(dane[0])
            lokalizacja = mapa_kompanii.get(komp_int, "Nieznana")
        except Exception:
            messagebox.showerror("Błąd", "Kompania musi być liczbą od 1 do 8")
            return

        conn = connect_db()
        c = conn.cursor()
        if current_table == "kadra":
            c.execute("INSERT INTO kadra (kompania, lokalizacja, pluton, stopien, imie, nazwisko) VALUES (?, ?, ?, ?, ?, ?)",
                      (komp_int, lokalizacja, dane[1], dane[2], dane[3], dane[4]))
        else:
            c.execute("INSERT INTO pchorki (kompania, lokalizacja, pluton, imie, nazwisko) VALUES (?, ?, ?, ?, ?)",
                      (komp_int, lokalizacja, dane[1], dane[2], dane[3]))
        conn.commit()
        conn.close()
        nowe_okno.destroy()
        odswiez()

    tk.Button(nowe_okno, text="Dodaj", command=zapisz, bg=btn_bg, fg=btn_fg, activebackground=highlight_color).grid(row=len(labels), column=0, columnspan=2, pady=10)

tk.Button(frame_buttons, text="Podchorążowie", width=20, command=lambda: pokaz_tabele("pchorki"), bg=btn_bg, fg=btn_fg, activebackground=highlight_color).pack(side='left', padx=20)
tk.Button(frame_buttons, text="Kadra", width=20, command=lambda: pokaz_tabele("kadra"), bg=btn_bg, fg=btn_fg, activebackground=highlight_color).pack(side='left', padx=20)

okno.mainloop()
