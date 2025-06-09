from tkinter import *

import tkintermapview

users:list = []
class User:
    def __init__(self, name, surname, location, posts):
        self.name = name
        self.surname = surname
        self.location = location
        self.posts = posts
        self.coordinates = self.get_coordinates()
        self.marker = map_vidget.set_marker(self.coordinates[0], self.coordinates[1])


    def get_coordinates(self)->list:
        import requests
        from bs4 import BeautifulSoup
        address_url:str=f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude:float=float(response_html.select(".longitude")[1].text.replace(",","."))
        # print(longitude)
        latitude:float=float(response_html.select(".latitude")[1].text.replace(",","."))
        # print(latitude)
        return [latitude, longitude]





def add_user():
    imie = entry_name.get()
    nazwisko = entry_surname.get()
    posty = entry_post.get()
    miejscowosc = entry_location.get()
    tmp_user = (User(name=imie, surname=nazwisko, location=miejscowosc, posts=posty))
    users.append(tmp_user)



    print(users)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_post.delete(0, END)
    entry_location.delete(0, END)

    entry_name.focus()
    show_users()

def show_users():
    listbox_lista_obiektów.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektów.insert(idx, f'{idx+1}.{user.name} {user.surname} {user.location} {user.posts} ')


def remove_user():
    idx=listbox_lista_obiektów.index(ACTIVE)
    users[idx].marker.delete()
    users.pop(idx)
    show_users()

def user_details():
    idx=listbox_lista_obiektów.index(ACTIVE)
    label_name_szczegóły_obiektu_wartość.configure(text=users[idx].name)
    label_surname_szczegóły_obiektu_wartość.configure(text=users[idx].surname)
    label_post_szczegóły_obiektu_wartość.configure(text=users[idx].posts)
    label_location_szczegóły_obiektu_wartość.configure(text=users[idx].location)
    map_vidget.set_position(users[idx].coordinates[0], users[idx].coordinates[1])
    map_vidget.set_zoom(17)


def edit_user():
    idx=listbox_lista_obiektów.index(ACTIVE)
    entry_name.insert(0, users[idx].name)
    entry_surname.insert(0, users[idx].surname)
    entry_post.insert(0, users[idx].posts)
    entry_location.insert(0, users[idx].location)


    button_dodaj_obiekt.configure(text='Zapisz', command=lambda:update_users(idx))

def update_users(idx):
    name=entry_name.get()
    surname=entry_surname.get()
    posts=entry_post.get()
    location=entry_location.get()


    users[idx].name = name
    users[idx].surname = surname
    users[idx].posts = posts
    users[idx].location = location

    users[idx].marker.delete()


    users[idx].coordinates = users[idx].get_coordinates()
    users[idx].marker = map_vidget.set_marker(users[idx].coordinates[0],users[idx].coordinates[1])

    button_dodaj_obiekt.configure(text='Dodaj obiekt', command=add_user)

    show_users()



















root = Tk()
root.title("MapBook_ow")
root.geometry("1024x768")

# RAMKI
ramka_lista_obiektów = Frame(root)
ramka_formularz = Frame(root)
ramka_szcegóły_obiektów = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektów.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szcegóły_obiektów.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)


# RAMKA LISTA OBIEKTÓW

label_lista_obiektów = Label(ramka_lista_obiektów, text="LiStA ObIeKtÓw:")
label_lista_obiektów.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektów = Listbox(ramka_lista_obiektów)
listbox_lista_obiektów.grid(row=1, column=0, columnspan=3)
button_pokaż_szczegóły = Button(ramka_lista_obiektów, text="Pokaż szczegóły", command=user_details)
button_pokaż_szczegóły.grid(row=2, column=0)
button_edytuj_obiekt = Button(ramka_lista_obiektów, text="Edytuj obiekt", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=1)
button_usuń_obiekt = Button(ramka_lista_obiektów, text="Usuń obiekt", command=remove_user)
button_usuń_obiekt.grid(row=2, column=2)

# RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name = Label(ramka_formularz, text="Imię:  ")
label_name.grid(row=1, column=0, sticky=W)
label_surname = Label(ramka_formularz, text="Nazwisko:   ")
label_surname.grid(row=2, column=0, sticky=W)
label_post = Label(ramka_formularz, text="Liczba postów:   ")
label_post.grid(row=3, column=0, sticky=W)
label_location = Label(ramka_formularz, text="Miejscowość: ")
label_location.grid(row=4, column=0, sticky=W)


entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1,)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1,)
entry_post = Entry(ramka_formularz)
entry_post.grid(row=3, column=1,)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=4, column=1,)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj obiekt", command=add_user)
button_dodaj_obiekt.grid(row=5, column=1, columnspan=2)

# RAMKA SZCZEGÓŁY OBIEKTU
label_szczegóły_obiektu = Label(ramka_szcegóły_obiektów, text="Szczegóły użytkownika:")
label_szczegóły_obiektu.grid(row=0, column=0, sticky=W)

label_name_szczegóły_obiektu = Label(ramka_szcegóły_obiektów, text="Imię:   ")
label_name_szczegóły_obiektu.grid(row=1, column=0,)

label_name_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text=".....   ")
label_name_szczegóły_obiektu_wartość.grid(row=1, column=1, )

label_surname_szczegóły_obiektu_ = Label(ramka_szcegóły_obiektów, text="Nazwisko:   ")
label_surname_szczegóły_obiektu_.grid(row=1, column=2,)

label_surname_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text=".....   ")
label_surname_szczegóły_obiektu_wartość.grid(row=1, column=3, )

label_post_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text="Liczba postów:   ")
label_post_szczegóły_obiektu_wartość.grid(row=1, column=4, )

label_post_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text=".....   ")
label_post_szczegóły_obiektu_wartość.grid(row=1, column=5, )

label_location_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text="Miejscowość:   ")
label_location_szczegóły_obiektu_wartość.grid(row=1, column=6, )

label_location_szczegóły_obiektu_wartość = Label(ramka_szcegóły_obiektów, text=".....   ")
label_location_szczegóły_obiektu_wartość.grid(row=1, column=7, )


# RAMKA MAPA
map_vidget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400,)
map_vidget.set_position(52.23,21)
map_vidget.set_zoom(5)
map_vidget.grid(row=0, column=0, columnspan=8)



root.mainloop()