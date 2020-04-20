from funkcje import *
# -*- coding: utf-8 -*-



if __name__ == '__main__':

    link = '2016/GPS.xlsx'
    link1 = '2016/Chart 6_5_16 [0].csv'
    link2 = '2016/czasy.txt'
    link3 = '2016/par.txt'

    #Wczytane dane
    rozwiazanie, t_gps, X, Y, H = load_excel(link)
    depth ,t_sonda = load_sonda(link1)
    czas = load_czas(link2, 'Chart 6_5_16 [0]')
    roznica, wys_tyczki = load_par(link3)

    #Czas z pomiaru gps
    time_gps = [Time(str(t).split()[-1]) for t in t_gps ]

    #Godziny i indexy wybranych soundingów
    time = []
    for t in czas:
        li = t.split()
        index = int(li[1])-1
        tmp = Time(li[2])
        tmp.czas +=  roznica.czas
        time.append([index, tmp])


    #Czas pierwszego soundingu
    czas_zerowy = [obl_czas_zerowy(t,t_sonda) for t in time]
    czas_zerowy_sredni = czas_sredni(czas_zerowy)

    #Czasy soundingów
    time_sonda = []
    for t in t_sonda:
        tmp = Time()
        tmp.czas = czas_zerowy_sredni.czas + t/1000
        time_sonda.append(tmp)

    punkty = []
    #Przypisane współrzędneych soundingom
    for ind, i in enumerate(time_sonda[:150]):
        index = szukac_index(i,time_gps)
        if index != 'brak danych':
            tmp = Point(X=X[index],Y=Y[index], Hel=(H[index] - wys_tyczki - depth[ind]/3.2808), dok = rozwiazanie )
            punkty.append(tmp)


    print(39.764-39.747 )















