class JegyFoglalas:
    def __init__(self, utas_nev, jarat):
        self.utas_nev = utas_nev
        self.jarat = jarat

    def info(self):
        return f"{self.utas_nev} - {self.jarat.info()}"

class FoglalasKezelo:
    def __init__(self):
        self.foglalasok = []

    def foglalas_hozzaadasa(self, foglalas):
        self.foglalasok.append(foglalas)
        return foglalas.jarat.jegyar

    def lemondas(self, utas_nev, jaratszam):
        for f in self.foglalasok:
            if f.utas_nev == utas_nev and f.jarat.jaratszam == jaratszam:
                self.foglalasok.remove(f)
                return True
        return False

    def listaz_foglalasok(self):
        return [f.info() for f in self.foglalasok]
