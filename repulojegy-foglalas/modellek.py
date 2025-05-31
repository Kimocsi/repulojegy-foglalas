from PyQt5.QtCore import QDate

class Jarat:
    def __init__(self, jaratszam, celallomas, ar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.ar = ar

    def __str__(self):
        return f"{self.jaratszam} - {self.celallomas} ({self.ar} Ft)"

class BelfoldiJarat(Jarat):
    pass

class NemzetkoziJarat(Jarat):
    pass

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def hozzaad_jarat(self, jarat):
        self.jaratok.append(jarat)

class JegyFoglalas:
    def __init__(self, nev, jarat, idopont):
        self.nev = nev
        self.jarat = jarat
        self.idopont = idopont

    def __str__(self):
        datum_str = self.idopont.toString("yyyy.MM.dd")
        return f"{self.nev} - {self.jarat.jaratszam} ({self.jarat.celallomas}) - {datum_str}"
