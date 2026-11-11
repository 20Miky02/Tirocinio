import zlib

OUTPUT_FILE = "risultati_avanzati.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def separatore():
    scrivi("+" + "-"*10 + "+" + "-"*18 + "+" + "-"*30 + "+")

def riga_tabella(col1, col2, col3):
    scrivi("| %-8s | %-16s | %-28s |" % (col1, col2, col3))

REAL_SECRET  = "COOKIE=Pass99"
KNOWN_PREFIX = "COOKIE="
CHARSET      = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      AVANZATO 2 - Mappa completa del segnale su tutti i caratteri")
scrivi("="*70)
scrivi("")
scrivi("  Segreto reale:  " + REAL_SECRET)
scrivi("  Prefisso noto:  " + KNOWN_PREFIX)
scrivi("  Obiettivo:      scoprire il primo carattere dopo il prefisso")
scrivi("")

real_first = REAL_SECRET[len(KNOWN_PREFIX)]

size_map = {}
for char in CHARSET:
    payload          = KNOWN_PREFIX + char
    size_map[char]   = misura(REAL_SECRET, payload)

min_size  = min(size_map.values())
max_size  = max(size_map.values())
best_char = min(size_map, key=size_map.get)

separatore()
riga_tabella("Char", "Dim. pacchetto", "Segnale visivo")
separatore()

BAR_MAX = 24
for char in CHARSET:
    size = size_map[char]

    if max_size > min_size:
        bar_len = (size - min_size) * BAR_MAX / (max_size - min_size)
    else:
        bar_len = BAR_MAX

    bar    = "#" * bar_len
    marker = "<-- MATCH!" if char == real_first else ""
    riga_tabella("'%s'" % char, "%d byte" % size, "%-24s %s" % (bar, marker))

separatore()
scrivi("")
scrivi("  Carattere con pacchetto minimo: '%s' (%d byte)" % (best_char, min_size))
scrivi("  Carattere reale:                '%s'" % real_first)
scrivi("  Dimensione massima osservata:   %d byte" % max_size)
scrivi("  Segnale totale (max - min):     %d byte" % (max_size - min_size))

if best_char == real_first:
    scrivi("  Risultato: ATTACCO RIUSCITO")
else:
    scrivi("  Risultato: FALSO POSITIVO")

scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()