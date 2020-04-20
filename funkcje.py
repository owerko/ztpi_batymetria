import pandas as pd

"""Definicje klas obiektów"""

"""Klasa czas"""
class Time():

    def __init__(self,czas = "0:0:0"):
        czas = czas.split(':')
        self.czas = float(czas[0]) * 3600 + float(czas[1]) * 60 + float(czas[2])

    def __float__(self):
        return self.czas

    def __int__(self):
        return self.czas

    def __str__(self):
        g = int(self.czas / 3600)
        m = int((self.czas - g * 3600) / 60)
        s = self.czas - g * 3600 - m * 60
        t = '{:02d}:{:02d}:{:06.3f}'.format(g, m, s)
        return t

    def dodaj(self, t):
        self.czas = t


"""Klasa punkt"""
class Point():

    def __init__(self, X = 0, Y = 0, Hel = 0, H = 0, dok = "" ):
        self.X = X
        self.Y = Y
        self.Hel = Hel
        self.H = H
        self.dok = dok

"""Definicje funkcji"""

"""Wczytywanie pomiarowych sondy"""
def load_sonda(nazwa):
    data = pd.read_csv(nazwa)
    depth = data['Depth'].to_list()
    time = data['TimeOffset[ms]'].to_list()
    return depth, time

"""Wczytywanie danych pomiarowych GPS"""
def load_excel(nazwa):
    data = pd.read_excel(nazwa,'Arkusz1',header=None,)
    rozwiazanie=data[1].to_list()
    time = data[2].to_list()
    Y = data[3].to_list()
    X = data[4].to_list()
    H = data[5].to_list()
    return rozwiazanie, time, X, Y, H

"""Wczytywanie parametrow pomiaru"""
def load_par(nazwa):
    with open(nazwa,'r') as plik:
        li = plik.readlines()
        h = float(li[1].rstrip().lstrip())
        t = li[3].rstrip().lstrip()
        t=Time(t)
    return t, h

"""Wczytywanie czasów wybranych soundingów"""
def load_czas(nazwa, nazwa_sondowania):
    czas = []
    tmp = False
    son = nazwa_sondowania.split('.')[0]
    with open(nazwa, 'r') as plik:
        linie = plik.readlines()
        for li in linie:
            li=li.rstrip()
            li=li.lstrip()
            if li == son:
                tmp = True
                continue
            if tmp:
                if li == '':
                    break
                else:
                    czas.append(li)
    return czas

"""Obliczenie czasu zerowego na podstawie wybranego soundingu"""
def obl_czas_zerowy(zero, saund):
    zerowy = Time()
    zerowy.czas = zero[1].czas - saund[zero[0]] / 1000
    return  zerowy

"""Obliczenie czsu sredniego"""
def czas_sredni(lista):
    suma = 0
    for i in lista:
        suma += i.czas
    t = Time()
    t.czas = suma / len(lista)
    return t


def printt(lista):
    for i in lista:
        print(i)

#Wyszukiwanie określonego czasu
def szukac_czasu(lista,czas):
    index = 0
    zwrot = 'brak danych'
    for li in lista:
        if li.czas == czas:
            zwrot = index
            break
        index += 1
    return zwrot

def szukac_index(i,time_gps):
    if (i.czas - int(i.czas)) <= 0.5:
        index = szukac_czasu(time_gps, int(i.czas))
        if index == 'brak danych':
            index = szukac_czasu(time_gps, int(i.czas) + 1)
    else:
        index = szukac_czasu(time_gps, int(i.czas) + 1)
        if index == 'brak danych':
            index = szukac_czasu(time_gps, int(i.czas))
    return  index

