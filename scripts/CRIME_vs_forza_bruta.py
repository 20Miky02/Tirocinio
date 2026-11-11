import zlib

OUTPUT_FILE = "risultati_avanzati.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def sep_2():
    scrivi("+" + "-"*42 + "+" + "-"*28 + "+")

def riga_2(col1, col2):
    scrivi("| %-40s | %-26s |" % (col1, col2))

def sep_att():
    scrivi("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*14 + "+")

def riga_att(col1, col2, col3, col4):
    scrivi("| %-10s | %-14s | %-14s | %-12s |" % (col1, col2, col3, col4))

REAL_SECRET          = "COOKIE=Tk9z"
KNOWN_PREFIX         = "COOKIE="
CHARSET              = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SECRET_SUFFIX_LENGTH = 4

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      AVANZATO 3 - CRIME vs Forza Bruta: confronto di efficienza")
scrivi("="*70)
scrivi("")
scrivi("  Segreto da scoprire: %d caratteri dopo '%s'" % (SECRET_SUFFIX_LENGTH, KNOWN_PREFIX))
scrivi("  Alfabeto:            %d caratteri possibili" % len(CHARSET))
scrivi("")

# Calcoli teorici
charset_size  = len(CHARSET)
brute_force   = charset_size ** SECRET_SUFFIX_LENGTH
crime_max     = charset_size * SECRET_SUFFIX_LENGTH

scrivi(">> CALCOLO TEORICO")
scrivi("-" * 70)
sep_2()
riga_2("Metodo", "Tentativi necessari")
sep_2()
riga_2("Forza bruta (caso peggiore)", "%d" % brute_force)
riga_2("CRIME (caso peggiore teorico)", "%d" % crime_max)
sep_2()
scrivi("")

# Attacco CRIME reale
scrivi(">> ATTACCO CRIME IN CORSO")
scrivi("-" * 70)

sep_att()
riga_att("Posizione", "Char trovato", "Dim. minima", "Tentativi")
sep_att()

secret_suffix  = REAL_SECRET[len(KNOWN_PREFIX):]
discovered     = ""
total_attempts = 0
correct        = 0

for pos in range(SECRET_SUFFIX_LENGTH):
    known_so_far = KNOWN_PREFIX + discovered
    min_size     = 99999
    best_char    = "?"
    attempts     = 0

    for char in CHARSET:
        size           = misura(REAL_SECRET, known_so_far + char)
        attempts      += 1
        total_attempts += 1
        if size < min_size:
            min_size  = size
            best_char = char

    real_char = secret_suffix[pos]
    if best_char == real_char:
        correct += 1
    discovered += best_char

    riga_att(
        "Pos. %d" % (pos + 1),
        "'%s'" % best_char,
        "%d byte" % min_size,
        "%d" % attempts
    )

sep_att()

# Confronto finale
accuratezza = correct * 100 / SECRET_SUFFIX_LENGTH
efficienza  = brute_force / total_attempts

scrivi("")
scrivi(">> CONFRONTO FINALE")
scrivi("-" * 70)
sep_2()
riga_2("Metodo", "Tentativi effettuati")
sep_2()
riga_2("Forza bruta totale (teorico)", "%d" % brute_force)
riga_2("CRIME - caso peggiore teorico", "%d" % crime_max)
riga_2("CRIME - tentativi reali", "%d" % total_attempts)
sep_2()
scrivi("")
scrivi("  Segreto reale:       " + REAL_SECRET)
scrivi("  Segreto ricostruito: " + KNOWN_PREFIX + discovered)
scrivi("  Accuratezza:         %d%%" % accuratezza)
scrivi("  CRIME e' stato %d volte piu' veloce della forza bruta." % efficienza)
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()