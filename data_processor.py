import sqlite3
from datetime import datetime

def inicializet_sistemu():
    conn = sqlite3.connect('balticdesk.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pieteikumi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            saņemšanas_laiks TEXT,
            avots TEXT,
            saturs TEXT,
            kategorija TEXT,
            statuss TEXT
        )
    ''')
    conn.commit()
    conn.close()

def saņemt_klienta_pieteikumu(avots, ziņas_saturs):
    conn = sqlite3.connect('balticdesk.db')
    cursor = conn.cursor()
    laiks_tagad = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    saturs_lower = ziņas_saturs.lower()
    
    if "rēķins" in saturs_lower or "apmaksa" in saturs_lower:
        kategorija = "Finanšu jautājums"
        statuss = "Apstrādāts automatizēti"
    elif "statuss" in saturs_lower or "kur ir" in saturs_lower:
        kategorija = "Statusa pieprasījums"
        statuss = "Apstrādāts automatizēti"
    else:
        kategorija = "Neklasificēts / Nestandarta"
        statuss = "Gaida darbinieka pārbaudi"
        print(f"🚨 [MS TEAMS ALERT] Jauns neklasificēts pieteikums no avota [{avots}] nodots manuālai izskatīšanai.")

    cursor.execute('''
        INSERT INTO pieteikumi (saņemšanas_laiks, avots, saturs, kategorija, statuss)
        VALUES (?, ?, ?, ?, ?)
    ''', (laiks_tagad, avots, ziņas_saturs, kategorija, statuss))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializet_sistemu()
    saņemt_klienta_pieteikumu("e-pasts", "Labdien, lūdzu atsūtiet man šī mēneša rēķinu.")
    saņemt_klienta_pieteikumu("MS Teams", "Man sistēmā parādījās kļūda 500.")
