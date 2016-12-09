# -*- coding: utf-8 -*-

from osoba import *

def main():
    D = Dzak("Teodora", "Šarlamanova", 2003, 6, 22, "ul. Vasil Surčev br. 29", "Vidoe Podgorec", "9-b", 1)
    D2 = Dzak("Ivan", "Ristov", 2004, 3, 13 , "ul. Mladinska br. 8", "Vidoe Podgorec", "8-a", 2)

    Z = Zaposlen("Katerina", "Šarlamanova", 1993, 10, 2 , "ul. Vasil Surčev br. 29" , "Geo-Prem" , None)

    D.info()
    D.odelenje()
    D.obnovio()
    D2.info()
    D2.obnovio()

    Z.info()
    Z.radi(2013,6,5,2013,12,5)
    Z.radi(2015,10,12,2016,10,28)
    Z.staz()

    #Kreiranje nov zaposlen preko unos podataka
    print "\nKreiranje nov zaposlen preko unos podataka"
    i = raw_input("Ime: ")
    p = raw_input("Prezme: ")
    y = int(input("Godina: "))
    m = int(input("Mesec: "))
    d = int(input("Den: "))
    a = raw_input("Adresa: ")
    k = raw_input("Kompanija: ")
    dep = raw_input("Department: ")
    r1 = input("Unesite godina kad se zaposlio: ")
    r2 = input("Unesite mesec kad se zaposlio: ")
    r3 = input("Unesite dan kad se zaposlio: ")
    r4 = input("Unesite godina kad je prekinuo: ")
    r5 = input("Unesite mesec kad je prekinuo: ")
    r6 = input("Unesite dan kad je prekinuo: ")

    o = Zaposlen(i, p, y, m, d, a, k, dep)
    o.info()
    o.radi(r1, r2, r3, r4, r5, r6)
    o.staz()

if __name__ == '__main__':
    main()