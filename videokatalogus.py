import os
import sys
import time

# Videokatalógus program Python verzió
# Eredeti: Commodore 64 BASIC V2
# VHS kazetták nyilvántartására készült

class VideoKatalogus:
    def __init__(self):
        # Inicializáljuk a kazetta tömböt
        # 200 kazetta, mindegyiken 31 hely (0. index a kazetta adataihoz, 1-30 a filmekhez)
        self.kazettak = [["" for _ in range(31)] for _ in range(201)]
        self.menukijelzes()
    
    def kepernyotorles(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def menukijelzes(self):
        while True:
            self.kepernyotorles()
            print("=" * 40)
            print("       VIDEOKATALÓGUS PROGRAM")
            print("=" * 40)
            print("1. Adatbevitel és javítás")
            print("2. Kírás kazettánként")
            print("3. Összes kazetta tartalom")
            print("4. Maradék idők listája")
            print("5. Helykeresés filmnek")
            print("6. Adatmentés lemezre")
            print("7. Adattöltés lemezről")
            print("8. Kazetta törlése")
            print("9. Program vége")
            print("=" * 40)
            
            try:
                valasztas = int(input("Válassz (1-9): "))
                if 1 <= valasztas <= 9:
                    if valasztas == 1:
                        self.adatbevitel()
                    elif valasztas == 2:
                        self.kiras_kazettankent()
                    elif valasztas == 3:
                        self.osszes_kazetta()
                    elif valasztas == 4:
                        self.maradek_idok()
                    elif valasztas == 5:
                        self.helykereses()
                    elif valasztas == 6:
                        self.adatmentes()
                    elif valasztas == 7:
                        self.adattoltes()
                    elif valasztas == 8:
                        self.kazetta_torlese()
                    elif valasztas == 9:
                        self.program_vege()
                else:
                    print("Hibás választás! Nyomj ENTER-t...")
                    input()
            except ValueError:
                print("Érvénytelen bemenet! Nyomj ENTER-t...")
                input()
    
    def adatbevitel(self):
        self.kepernyotorles()
        print("ADATBEVITEL ÉS JAVÍTÁS")
        print("-" * 40)
        
        try:
            sz = int(input("Kazettaszám (1-200): "))
            if sz < 1 or sz > 200:
                print("Hibás szám! Nyomj ENTER-t...")
                input()
                return
        except ValueError:
            print("Érvénytelen bemenet! Nyomj ENTER-t...")
            input()
            return
        
        knev = input("Kazettanév (max 28 karakter): ")
        if len(knev) > 28:
            knev = knev[:28]
        
        while True:
            try:
                kh = int(input("Kazettahossz percben (60-300): "))
                if 60 <= kh <= 300:
                    break
                print("60 és 300 közötti érték szükséges!")
            except ValueError:
                print("Számot adj meg!")
        
        ora = kh // 60
        perc = kh % 60
        print(f"Ez {ora} óra és {perc} perc")
        
        kh_str = str(kh).zfill(3)
        self.kazettak[sz][0] = f"{sz}/{knev}/{kh_str}"
        
        i = 1
        while i <= 30:
            print(f"{i}. film (üres sor = vége):")
            film = input()
            if film == "":
                break
            
            if len(film) > 28:
                film = film[:28]
            
            try:
                perc = int(input("Hossza percben (1-300): "))
                if perc < 1 or perc > 300:
                    print("1 és 300 közötti érték szükséges!")
                    continue
            except ValueError:
                print("Számot adj meg!")
                continue
            
            perc_str = str(perc).zfill(3)
            self.kazettak[sz][i] = f"{film}/{perc_str}"
            i += 1
    
    def kiras_kazettankent(self):
        self.kepernyotorles()
        print("KÍRÁS KAZETTÁNKÉNT")
        print("-" * 40)
        
        try:
            sz = int(input("Kazettaszám (1-200): "))
            if sz < 1 or sz > 200:
                print("Hibás szám! Nyomj ENTER-t...")
                input()
                return
            
            if self.kazettak[sz][0] == "":
                print(f"{sz}. kazetta nincs feltöltve! Nyomj ENTER-t...")
                input()
                return
        except ValueError:
            print("Érvénytelen bemenet! Nyomj ENTER-t...")
            input()
            return
        
        self.kepernyotorles()
        print(f"A(z) {sz}. kazetta tartalma:")
        print("-" * 40)
        
        kazetta_info = self.kazettak[sz][0].split('/')
        print(f"Kazetta neve: {kazetta_info[1]}")
        print(f"Kazetta hossza: {kazetta_info[2]} perc")
        print("-" * 40)
        
        hasznalt_perc = 0
        for i in range(1, 31):
            if self.kazettak[sz][i] != "":
                film_info = self.kazettak[sz][i].split('/')
                film_nev = film_info[0]
                film_hossz = int(film_info[1])
                hasznalt_perc += film_hossz
                print(f"{i}. {film_nev} ({film_hossz} perc)")
        
        ossz_perc = int(kazetta_info[2])
        maradek_perc = ossz_perc - hasznalt_perc
        print("-" * 40)
        print(f"Összesen felhasznált: {hasznalt_perc} perc")
        print(f"Összes hossz: {ossz_perc} perc")
        print(f"Maradék idő: {maradek_perc} perc")
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def osszes_kazetta(self):
        self.kepernyotorles()
        print("ÖSSZES KAZETTA TARTALMA")
        print("-" * 60)
        
        volt_kazetta = False
        for sz in range(1, 201):
            if self.kazettak[sz][0] != "":
                volt_kazetta = True
                kazetta_info = self.kazettak[sz][0].split('/')
                print(f"{sz}. Kazetta: {kazetta_info[1]} ({kazetta_info[2]} perc)")
                
                film_van = False
                for i in range(1, 31):
                    if self.kazettak[sz][i] != "":
                        film_van = True
                        film_info = self.kazettak[sz][i].split('/')
                        print(f"   {i}. {film_info[0]} ({film_info[1]} perc)")
                
                if not film_van:
                    print("   [Nincs film a kazettán]")
                print("-" * 40)
        
        if not volt_kazetta:
            print("Nincs rögzített kazetta az adatbázisban!")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def maradek_idok(self):
        self.kepernyotorles()
        print("MARADÉK IDŐK LISTÁJA")
        print("-" * 40)
        
        volt_kazetta = False
        for sz in range(1, 201):
            if self.kazettak[sz][0] != "":
                volt_kazetta = True
                kazetta_info = self.kazettak[sz][0].split('/')
                ossz_perc = int(kazetta_info[2])
                
                hasznalt_perc = 0
                for i in range(1, 31):
                    if self.kazettak[sz][i] != "":
                        film_info = self.kazettak[sz][i].split('/')
                        film_hossz = int(film_info[1])
                        hasznalt_perc += film_hossz
                
                maradek_perc = ossz_perc - hasznalt_perc
                print(f"{sz}. Kazetta: {kazetta_info[1]} - Maradék idő: {maradek_perc} perc")
        
        if not volt_kazetta:
            print("Nincs rögzített kazetta az adatbázisban!")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def helykereses(self):
        self.kepernyotorles()
        print("HELYKERESÉS FILMNEK")
        print("-" * 40)
        
        try:
            film_hossz = int(input("Felveendő film hossza percben: "))
            if film_hossz < 1 or film_hossz > 300:
                print("1 és 300 közötti érték szükséges! Nyomj ENTER-t...")
                input()
                return
        except ValueError:
            print("Érvénytelen bemenet! Nyomj ENTER-t...")
            input()
            return
        
        self.kepernyotorles()
        print(f"Keresés {film_hossz} perces filmhez...")
        print("-" * 40)
        
        talalat = False
        for sz in range(1, 201):
            if self.kazettak[sz][0] != "":
                kazetta_info = self.kazettak[sz][0].split('/')
                ossz_perc = int(kazetta_info[2])
                
                hasznalt_perc = 0
                for i in range(1, 31):
                    if self.kazettak[sz][i] != "":
                        film_info = self.kazettak[sz][i].split('/')
                        film_hossz_kazetta = int(film_info[1])
                        hasznalt_perc += film_hossz_kazetta
                
                maradek_perc = ossz_perc - hasznalt_perc
                
                if maradek_perc >= film_hossz:
                    talalat = True
                    print(f"{sz}. Kazetta: {kazetta_info[1]} - Maradék idő: {maradek_perc} perc")
        
        if not talalat:
            print("Nem található megfelelő kazetta a film számára!")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def adatmentes(self):
        self.kepernyotorles()
        print("ADATMENTÉS LEMEZRE")
        print("Dolgozom...")
        
        try:
            with open("videoortas.dat", "w") as f:
                for sz in range(1, 201):
                    if self.kazettak[sz][0] != "":
                        f.write(f"{self.kazettak[sz][0]}\n")
                        
                        for i in range(1, 31):
                            if self.kazettak[sz][i] != "":
                                f.write(f"{self.kazettak[sz][i]}\n")
                        
                        f.write("FV\n")  # Film vége jelölés
                
                f.write("KV\n")  # Kazetta vége jelölés
            
            print("Adatmentés sikeres!")
        except Exception as e:
            print(f"Hiba az adatmentés során: {e}")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def adattoltes(self):
        self.kepernyotorles()
        print("ADATTÖLTÉS LEMEZRŐL")
        print("Dolgozom...")
        
        self.kazettak = [["" for _ in range(31)] for _ in range(201)]
        
        try:
            if not os.path.exists("videoortas.dat"):
                print("A fájl nem található!")
                print("\nNyomj ENTER-t a folytatáshoz...")
                input()
                return
                
            with open("videoortas.dat", "r") as f:
                sz = 1
                i = 0
                
                for line in f:
                    line = line.strip()
                    
                    if line == "KV":
                        break
                    
                    if line == "FV":
                        sz += 1
                        i = 0
                        continue
                    
                    if i == 0:
                        self.kazettak[sz][0] = line
                        i += 1
                    else:
                        self.kazettak[sz][i] = line
                        i += 1
            
            print("Adattöltés sikeres!")
        except Exception as e:
            print(f"Hiba az adattöltés során: {e}")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def kazetta_torlese(self):
        self.kepernyotorles()
        print("KAZETTA TÖRLÉSE")
        print("-" * 40)
        
        try:
            sz = int(input("Törlendő kazetta száma (1-200): "))
            if sz < 1 or sz > 200:
                print("Hibás szám! Nyomj ENTER-t...")
                input()
                return
            
            if self.kazettak[sz][0] == "":
                print(f"{sz}. kazetta nem létezik! Nyomj ENTER-t...")
                input()
                return
        except ValueError:
            print("Érvénytelen bemenet! Nyomj ENTER-t...")
            input()
            return
        
        kazetta_info = self.kazettak[sz][0].split('/')
        valasz = input(f"Biztosan törli a(z) {sz}. kazettát ({kazetta_info[1]})? (I/N): ")
        
        if valasz.upper() == "I":
            for i in range(31):
                self.kazettak[sz][i] = ""
            print(f"A(z) {sz}. kazetta törölve!")
        else:
            print("Törlés megszakítva!")
        
        print("\nNyomj ENTER-t a folytatáshoz...")
        input()
    
    def program_vege(self):
        self.kepernyotorles()
        print("PROGRAM VÉGE")
        print("-" * 40)
        
        valasz = input("Kilép a programból? (I/N): ")
        if valasz.upper() == "I":
            print("Viszontlátásra!")
            time.sleep(1)
            sys.exit(0)
        else:
            return

# Program indítása
if __name__ == "__main__":
    app = VideoKatalogus()