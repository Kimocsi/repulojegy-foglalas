import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QListWidget, QMessageBox, QLineEdit, QDateEdit
)
from PyQt5.QtCore import QDate
from modellek import BelfoldiJarat, NemzetkoziJarat, LegiTarsasag, JegyFoglalas

class FoglalasiRendszer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Repülőjegy Foglalás")

        self.legi_tarsasagok = []
        self.foglalasok = []

        self.initUI()
        self.initAdatok()

    def initUI(self):
        layout = QVBoxLayout()

        self.nev_input = QLineEdit()
        self.nev_input.setPlaceholderText("Utazó neve")

        self.datum_valaszto = QDateEdit()
        self.datum_valaszto.setDate(QDate.currentDate())
        self.datum_valaszto.setMinimumDate(QDate.currentDate())
        self.datum_valaszto.setCalendarPopup(True)

        self.jarat_combo = QComboBox()

        self.foglalas_btn = QPushButton("Jegy foglalása")
        self.foglalas_btn.clicked.connect(self.foglalas)

        self.listaz_btn = QPushButton("Foglalások listázása")
        self.listaz_btn.clicked.connect(self.listaz_foglalasokat)

        self.list_widget = QListWidget()

        self.lemondas_btn = QPushButton("Kiválasztott foglalás lemondása")
        self.lemondas_btn.clicked.connect(self.lemondas)

        layout.addWidget(QLabel("Utazó neve:"))
        layout.addWidget(self.nev_input)

        layout.addWidget(QLabel("Foglalás dátuma:"))
        layout.addWidget(self.datum_valaszto)

        layout.addWidget(QLabel("Válassz egy járatot:"))
        layout.addWidget(self.jarat_combo)
        layout.addWidget(self.foglalas_btn)
        layout.addWidget(self.listaz_btn)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.lemondas_btn)

        self.setLayout(layout)

    def initAdatok(self):
        wizz = LegiTarsasag("WizzAir")
        ryanair = LegiTarsasag("Ryanair")

        # WizzAir járatok
        wizz.hozzaad_jarat(BelfoldiJarat("W101", "Budapest", 12000))
        wizz.hozzaad_jarat(BelfoldiJarat("W102", "Debrecen", 10000))
        wizz.hozzaad_jarat(NemzetkoziJarat("W201", "London", 30000))
        wizz.hozzaad_jarat(NemzetkoziJarat("W202", "Róma", 28000))  # 4. járat

        # Ryanair járatok
        ryanair.hozzaad_jarat(BelfoldiJarat("R103", "Pécs", 11000))
        ryanair.hozzaad_jarat(NemzetkoziJarat("R202", "Párizs", 35000))
        ryanair.hozzaad_jarat(NemzetkoziJarat("R203", "Berlin", 32000))

        self.legi_tarsasagok.extend([wizz, ryanair])

        # Járatok betöltése a comboboxba
        for tarsasag in self.legi_tarsasagok:
            for jarat in tarsasag.jaratok:
                self.jarat_combo.addItem(str(jarat), jarat)

        # Előre feltöltött 6 foglalás
        self.foglalasok.append(JegyFoglalas("Kovács Béla", wizz.jaratok[0], QDate.currentDate().addDays(2)))
        self.foglalasok.append(JegyFoglalas("Nagy Anna", ryanair.jaratok[1], QDate.currentDate().addDays(5)))
        self.foglalasok.append(JegyFoglalas("Tóth Sára", wizz.jaratok[1], QDate.currentDate().addDays(3)))
        self.foglalasok.append(JegyFoglalas("Kiss Máté", wizz.jaratok[3], QDate.currentDate().addDays(4)))  # most már létezik!
        self.foglalasok.append(JegyFoglalas("Fekete János", ryanair.jaratok[0], QDate.currentDate().addDays(6)))
        self.foglalasok.append(JegyFoglalas("Horváth Zsuzsa", ryanair.jaratok[2], QDate.currentDate().addDays(7)))

    def foglalas(self):
        nev = self.nev_input.text().strip()
        jarat = self.jarat_combo.currentData()
        datum = self.datum_valaszto.date()

        if not nev:
            QMessageBox.warning(self, "Hiba", "Adj meg egy nevet!")
            return

        if datum < QDate.currentDate():
            QMessageBox.warning(self, "Hibás dátum", "Csak jövőbeli dátumra lehet foglalni!")
            return

        uj_foglalas = JegyFoglalas(nev, jarat, datum)
        self.foglalasok.append(uj_foglalas)
        QMessageBox.information(self, "Sikeres foglalás", f"Sikeresen lefoglaltad a jegyet: {jarat}\n{datum.toString('yyyy.MM.dd')}")
        self.nev_input.clear()

    def listaz_foglalasokat(self):
        self.list_widget.clear()
        for foglalas in self.foglalasok:
            self.list_widget.addItem(str(foglalas))

    def lemondas(self):
        kivalasztott = self.list_widget.currentRow()
        if kivalasztott >= 0:
            torolt = self.foglalasok.pop(kivalasztott)
            self.listaz_foglalasokat()
            QMessageBox.information(self, "Lemondva", f"{torolt.nev} foglalása le lett mondva.")
        else:
            QMessageBox.warning(self, "Hiba", "Előbb válassz ki egy foglalást a listából!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ablak = FoglalasiRendszer()
    ablak.show()
    sys.exit(app.exec_())
