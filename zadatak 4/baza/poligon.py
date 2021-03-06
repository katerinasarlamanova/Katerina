# -*- coding: utf-8 -*-
#!/usr/bin/env python

from detalnjaTacka import *
import psycopg2
import psycopg2.extras

class Poligon:

    tacka = DetalnjaTacka(None, "", 2, None)

    def __init__(self, id):
        self._id = id
        self._wkt = "polygon"
        self.povrs = []

    def dodajTacka(self, tacka):
        self.tacka = tacka
        self.povrs.append(self.tacka)

    def __str__(self):
        return "ID_poligon: %s \nBr tacaka: %s \nKoolekcija tacaka: %s \nPovršina: %s" %(self.id, self.br(), self.povrs, self.areaPoligona())

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def wkt(self):
        return self._wkt

    @wkt.setter
    def wkt(self, wkt):
        self._wkt = wkt

    def br(self):
        return len(self.povrs)

    def areaPoligona(self):
        m = len(self.povrs)
        self.area = 0.0
        self.koordinate = []
        for i in range(m):
            k = self.povrs[i].koor
            self.koordinate.append(k)
        n = len(self.koordinate)
        for i in range(n):
            j = (i + 1) % n
            self.area += self.koordinate[i][0] * self.koordinate[j][1]
            self.area -= self.koordinate[j][0] * self.koordinate[i][1]
        self.area = abs(self.area) / 2.0
        return self.area


class Parcela(Poligon):

    def __init__(self, id, idp, oznaka, nacin):
        Poligon.__init__(self, id)
        self._idp = idp
        self._oznaka = oznaka
        self._nacin = nacin

    def __str__(self):
        return Poligon.__str__(self) + ("\nID_parcela: %s \nOznaka: %s \nNacin koriscenja: %s" %(self.idp, self.oznaka, self.nacin))

    @property
    def idp(self):
        return self._idp

    @idp.setter
    def idp(self, idp):
        self._idp = idp

    @property
    def oznaka(self):
        return self._oznaka

    @oznaka.setter
    def oznaka(self, oznaka):
        self._oznaka = oznaka

    @property
    def nacin(self):
        return self._nacin

    @nacin.setter
    def nacin(self, nacin):
        self._nacin = nacin


def main():

    p1 = DetalnjaTacka(3, "t2", 1, (2, 22))
    p2 = DetalnjaTacka(4, "t2", 2, (5, 6))
    p3 = DetalnjaTacka(5, "t2", 2, (2, 20))
    print "\n", p1
    print "\n", p2
    print "\n", p3

    par = Parcela(2, 8, "1881/1", 112)

    par.dodajTacka(p1)
    par.dodajTacka(p2)
    par.dodajTacka(p3)
    print "\n", par

    conn_string = "dbname='python' user='postgres' host='localhost' password='teodora2001'"
    print "\nConnecting to database\n	->%s" % (conn_string)

    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    query = ("""INSERT INTO parcela (id_parcela, brojparcele, nacinkoriscenja) VALUES (%s, %s, %s);""")
    data = (str(par.idp), str(par.oznaka), str(par.nacin))

    try:
        cursor.execute(query, data)
        conn.commit()

    except:
         print "\nNeuspesno ubacivanje podataka u tabelu parcela"

    m = len(par.povrs)
    for i in range(m):
        query2 = ("""INSERT INTO tacka (id_tacka, oznaka, nacinstabilizacija, koordinate) VALUES (%s, %s, %s, %s);""")
        data2 = (str(par.povrs[i].id), str(par.povrs[i].oznaka), str(par.povrs[i].stabil), str(par.povrs[i].koor))

        join = ("""INSERT INTO tackeparcela (id_parcela, id_tacka) VALUES (%s, %s);""")
        ids = (str(par.idp), str(par.povrs[i].id))

        try:
            cursor.execute(query2, data2)
            cursor.execute(join, ids)
            conn.commit()

        except: #(Exception, psycopg2.DatabaseError) as error: print(error)
            print "\nNeuspesno ubacivanje podataka u tabelu tacka"
            print "\nNeuspesno ubacivanje podataka u tabelu tackeparcela"

if __name__ == "__main__":
    main()