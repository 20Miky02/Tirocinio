import zlib

OUTPUT_FILE = "risultati_semplici.txt"

def misura(payload):
    return len(zlib.compress(payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def separatore():
    scrivi("+" + "-"*22 + "+" + "-"*16 + "+" + "-"*24 + "+")

def riga_tabella(col1, col2, col3):
    scrivi("| %-20s | %-14s | %-22s |" % (col1, col2, col3))

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      GRUPPO 1 - Carattere singolo vs ripetizione crescente")
scrivi("="*70)
scrivi("")

separatore()
riga_tabella("Payload inviato", "Byte osservati", "Crescita vs precedente")
separatore()

payloads = [
    ("1 x A",  "A"),
    ("2 x A",  "AA"),
    ("4 x A",  "AAAA"),
    ("8 x A",  "AAAAAAAA"),
    ("16 x A", "AAAAAAAAAAAAAAAA"),
    ("32 x A", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
]

prev = 0
for label, payload in payloads:
    size = misura(payload)
    if prev == 0:
        crescita = "(baseline)"
    else:
        crescita = "+%d byte" % (size - prev)
    riga_tabella(label, "%d byte" % size, crescita)
    prev = size

separatore()
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()