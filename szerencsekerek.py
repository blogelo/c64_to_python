import random
import time

class SzerencseKerek:
    def __init__(self):
        self.feladvanyok = [
            ("PYTHON PROGRAMOZASI NYELV", "informatika", 15),
            ("KOMMODOR VIKTOR", "történelmi személyiség", 12)
        ]
        self.kereso = [
            (100, 1), (200, 1), (300, 1), (400, 1), (500, 1),
            (750, 2), (1000, 2), (1500, 2), (2000, 3), ("CSŐD", 0),
            ("FELEZŐ", 0), (500, 1), (750, 1), (1000, 1), (2000, 2)
        ]
        self.jatekosok = []
        self.ossz_pontszam = [0, 0]

    def jatek_inditas(self):
        print("Üdvözöljük a Szerencsekerék játékban!")
        self.jatekosok.append(input("1. játékos neve: ")[:10])
        self.jatekosok.append(input("2. játékos neve: ")[:10])
        
        for fordulo in range(3):
            self.fordulo(fordulo+1)
        
        self.eredmeny_kijelzo()

    def fordulo(self, szam):
        print(f"\n=== {szam}. forduló ===")
        feladvany = random.choice(self.feladvanyok)
        titkositott = ['_' if c.isalpha() and c not in 'AÁEÉIÍOÓÖŐUÚÜŰ' else c for c in feladvany[0]]
        hasznalt_betuk = set()
        aktualis_jatekos = 0
        
        while True:
            print(f"\n{self.jatekosok[aktualis_jatekos]} következik")
            print(' '.join(titkositott))
            print(f"Feladvány típusa: {feladvany[1]}")
            
            valasztas = input("Pörgetés (P), Megfejtés (M), vagy Kilépés (Q): ").upper()
            if valasztas == 'Q':
                print("Kilépés a játékból. Viszlát!")
                exit()
            if valasztas == 'P':
                eredmeny, szorzo = random.choice(self.kereso)
                print(f"Pörgetett érték: {eredmeny}")
                
                if eredmeny == "CSŐD":
                    self.ossz_pontszam[aktualis_jatekos] = 0
                    print(f"{self.jatekosok[aktualis_jatekos]} minden pontját elvesztette!")
                    aktualis_jatekos = 1 - aktualis_jatekos
                    continue  # Nem szakítjuk meg a játékmenetet, csak játékost váltunk
                elif eredmeny == "FELEZŐ":
                    self.ossz_pontszam[aktualis_jatekos] //= 2
                    print(f"{self.jatekosok[aktualis_jatekos]} pontjai megfeleződtek!")
                    print(f"Új pontszám: {self.ossz_pontszam[aktualis_jatekos]}")
                    aktualis_jatekos = 1 - aktualis_jatekos
                    continue  # Nem szakítjuk meg a játékmenetet, csak játékost váltunk
                
                start_time = time.time()
                while True:
                    betu = input("Adj meg egy mássalhangzót: ").upper()
                    if time.time() - start_time > 25:
                        print("Időkorlát lejárt!")
                        aktualis_jatekos = 1 - aktualis_jatekos
                        break
                    if self.ervenyes_betu(betu, hasznalt_betuk):
                        hasznalt_betuk.add(betu)  # csak itt adjuk hozzá!
                        break
                    else:
                        print("Érvénytelen betű! Újra:")
                
                talalat = self.betu_ellenorzes(feladvany[0], betu, titkositott)
                if talalat > 0:
                    self.ossz_pontszam[aktualis_jatekos] += eredmeny * szorzo * talalat
                    print(f"Találat! Új pontszám: {self.ossz_pontszam[aktualis_jatekos]}")
                    
                    # Ellenőrizzük, hogy minden betűt kitaláltak-e már
                    if self.minden_massalhangzo_kitalalt(feladvany[0], titkositott):
                        print("Minden mássalhangzót kitaláltál!")
                        return
                else:
                    print("Nem tartalmazza a betűt!")
                    aktualis_jatekos = 1 - aktualis_jatekos
                    
            elif valasztas == 'M':
                tipp = input("Add meg a teljes megfejtést: ").upper()
                if tipp == feladvany[0]:
                    print("Helyes megfejtés!")
                    for i in range(len(feladvany[0])):
                        titkositott[i] = feladvany[0][i]
                    print(' '.join(titkositott))
                    
                    # Bónusz pont a helyes megfejtésért
                    self.ossz_pontszam[aktualis_jatekos] += 1000
                    print(f"Bónusz: +1000 pont! Összpontszám: {self.ossz_pontszam[aktualis_jatekos]}")
                    return
                else:
                    print("Hibás megfejtés!")
                    aktualis_jatekos = 1 - aktualis_jatekos

    def minden_massalhangzo_kitalalt(self, feladvany, titkositott):
        """Ellenőrzi, hogy minden mássalhangzót kitaláltak-e már"""
        for i, c in enumerate(feladvany):
            if c.isalpha() and c not in 'AÁEÉIÍOÓÖŐUÚÜŰ' and titkositott[i] == '_':
                return False
        return True

    def betu_ellenorzes(self, feladvany, betu, titkositott):
        talalat = 0
        for i in range(len(feladvany)):
            if feladvany[i] == betu:
                titkositott[i] = betu
                talalat += 1
        return talalat

    def ervenyes_betu(self, betu, hasznalt):
        if len(betu) != 1 or not betu.isalpha():
            print("Kérlek egy betűt adj meg!")
            return False
        if betu in 'AÁEÉIÍOÓÖŐUÚÜŰ':
            print("Csak mássalhangzót adhatsz meg!")
            return False
        if betu in hasznalt:
            print("Ezt már kitaláltad!")
            return False
        return True

    def eredmeny_kijelzo(self):
        print("\n=== Végeredmény ===")
        for i in range(2):
            print(f"{self.jatekosok[i]}: {self.ossz_pontszam[i]} pont")
        
        if self.ossz_pontszam[0] > self.ossz_pontszam[1]:
            nyertes = 0
        elif self.ossz_pontszam[0] < self.ossz_pontszam[1]:
            nyertes = 1
        else:
            print("Döntetlen!")
            return
            
        print(f"\nA nyertes: {self.jatekosok[nyertes]}!")

if __name__ == "__main__":
    jatek = SzerencseKerek()
    jatek.jatek_inditas()
