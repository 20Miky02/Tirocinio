import zlib

OUTPUT_FILE = "risultati_semplici.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def separatore():
    scrivi("+" + "-"*22 + "+" + "-"*16 + "+" + "-"*17 + "+")

def riga_tabella(col1, col2, col3):
    scrivi("| %-20s | %-14s | %-15s |" % (col1, col2, col3))

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      GRUPPO 3 - Confronto sistematico MATCH vs MISMATCH")
scrivi("="*70)
scrivi("")

SECRET  = "COOKIE=PASS123"
PREFIX  = "COOKIE="
CORRECT = "P"

scrivi("  Segreto: " + SECRET)
scrivi("  Carattere corretto: '" + CORRECT + "'")
scrivi("")

separatore()
riga_tabella("Payload inviato", "Byte osservati", "Esito")
separatore()

chars = ["A", "B", "P", "X", "Z", "1", "p", "Q"]

match_size    = 0
mismatch_size = 0

for char in chars:
    payload = PREFIX + char
    size    = misura(SECRET, payload)

    if char == CORRECT:
        esito      = "*** MATCH ***"
        match_size = size
    else:
        esito         = "mismatch"
        mismatch_size = size

    riga_tabella(payload, "%d byte" % size, esito)

separatore()
scrivi("")
scrivi("  Dimensione MATCH:    %d byte" % match_size)
scrivi("  Dimensione MISMATCH: %d byte" % mismatch_size)
scrivi("  Segnale:             %d byte" % (mismatch_size - match_size))
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()