import zlib

OUTPUT_FILE = "risultati_semplici.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def separatore():
    scrivi("+" + "-"*28 + "+" + "-"*16 + "+" + "-"*18+ "+")

def riga_tabella(col1, col2, col3):
    scrivi("| %-26s | %-14s | %-16s |" % (col1, col2, col3))

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      GRUPPO 2 - Seed del dizionario e match/mismatch progressivo")
scrivi("="*70)
scrivi("")

SECRET = "IL_MIO_COOKIE_E_SEGRETO"
scrivi("  Segreto usato: " + SECRET)
scrivi("")

separatore()
riga_tabella("Payload inviato", "Byte osservati", "Tipo")
separatore()

payloads = [
    ("IL_MIO_COOKIE_E_A",       "MISMATCH"),
    ("IL_MIO_COOKIE_E_S",       "MATCH"),
    ("IL_MIO_COOKIE_E_SE",      "MATCH"),
    ("IL_MIO_COOKIE_E_SEG",     "MATCH"),
    ("IL_MIO_COOKIE_E_SEGR",    "MATCH"),
    ("IL_MIO_COOKIE_E_SEGRE",   "MATCH"),
    ("IL_MIO_COOKIE_E_SEGRETO", "MATCH (completo)")
]

for payload, tipo in payloads:
    size = misura(SECRET, payload)
    riga_tabella(payload, "%d byte" % size, tipo)

separatore()
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()