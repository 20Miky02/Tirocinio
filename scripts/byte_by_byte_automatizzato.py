import zlib

OUTPUT_FILE = "risultati_avanzati.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def separatore():
    scrivi("+" + "-"*12 + "+" + "-"*12 + "-"*20 + "+" + "-"*14 + "+" + "-"*12 + "+")

def riga_tabella(col1, col2, col3, col4, col5):
    scrivi("| %-10s | %-10s | %-18s | %-12s | %-10s |" % (col1, col2, col3, col4, col5))

REAL_SECRET   = "COOKIE=Sess42xK"
KNOWN_PREFIX  = "COOKIE="
CHARSET       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=_-"

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      AVANZATO 1 - Attacco byte-by-byte automatizzato")
scrivi("="*70)
scrivi("")
scrivi("  Segreto reale (nascosto all'attaccante): " + REAL_SECRET)
scrivi("  Prefisso noto:                           " + KNOWN_PREFIX)
scrivi("  Caratteri nell'alfabeto:                 %d" % len(CHARSET))
scrivi("")

separatore()
riga_tabella("Posizione", "Char reale", "Dim. minima (byte)", "Char trovato", "Corretto?")
separatore()

secret_suffix = REAL_SECRET[len(KNOWN_PREFIX):]
discovered    = ""
correct       = 0
total         = 0

for pos in range(len(secret_suffix)):
    real_char    = secret_suffix[pos]
    known_so_far = KNOWN_PREFIX + discovered

    min_size  = 99999
    best_char = "?"

    for char in CHARSET:
        size   = misura(REAL_SECRET, known_so_far + char)
        total += 1
        if size < min_size:
            min_size  = size
            best_char = char

    ok = (best_char == real_char)
    if ok:
        correct += 1
    discovered += best_char

    riga_tabella(
        "Pos. %d" % (pos + 1),
        "'%s'" % real_char,
        "%d byte" % min_size,
        "'%s'" % best_char,
        "SI'" if ok else "NO"
    )

separatore()
scrivi("")
accuratezza = correct * 100 / len(secret_suffix)
scrivi("  Segreto reale:       " + REAL_SECRET)
scrivi("  Segreto ricostruito: " + KNOWN_PREFIX + discovered)
scrivi("  Caratteri corretti:  %d / %d (%d%%)" % (correct, len(secret_suffix), accuratezza))
scrivi("  Tentativi totali:    %d" % total)
scrivi("  Tentativi per char:  %d (dimensione alfabeto)" % len(CHARSET))
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()