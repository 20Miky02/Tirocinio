import zlib

OUTPUT_FILE = "risultati_semplici.txt"

def misura(secret, payload):
    return len(zlib.compress(secret + payload, 6))

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def sep_4():
    scrivi("+" + "-"*22 + "+" + "-"*15 + "+" + "-"*15 + "+" + "-"*10 + "+")

def riga_4(col1, col2, col3, col4):
    scrivi("| %-20s | %-13s | %-13s | %-8s |" % (col1, col2, col3, col4))

def sep_3():
    scrivi("+" + "-"*22 + "+" + "-"*16 + "+" + "-"*18)

def riga_3(col1, col2, col3):
    scrivi("| %-20s | %-14s | %-16s |" % (col1, col2, col3))

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      GRUPPO 4 - Lunghezza del segreto e intensita' del segnale")
scrivi("="*70)
scrivi("")

segreti = [
    ("CK=AB",               "CK="),
    ("COOK=ABCD",           "COOK="),
    ("COOKIE=ABCDEFGH",     "COOKIE="),
    ("COOKIE=ABCDEFGHIJKLMNO", "COOKIE=")
]

sep_4()
riga_4("Segreto", "Match (byte)", "Mismatch (byte)", "Segnale")
sep_4()

for secret, prefix in segreti:
    correct      = secret[len(prefix)]
    size_match   = misura(secret, prefix + correct)
    size_mismatch = misura(secret, prefix + "Z")
    diff         = size_mismatch - size_match
    riga_4(secret, "%d byte" % size_match, "%d byte" % size_mismatch, "+%d byte" % diff)

sep_4()

scrivi("")
scrivi("="*70)
scrivi("      GRUPPO 5 - Segreto con caratteri ripetuti (falsi positivi)")
scrivi("="*70)
scrivi("")

SECRET_5 = "COOKIE=AAABBBCCC"
scrivi("  Segreto usato: " + SECRET_5)
scrivi("")

chars  = ["A",              "B",              "C",              "D",        "Z"]
esiti  = ["MATCH (1° char)", "FALSO POSITIVO", "FALSO POSITIVO", "mismatch", "mismatch"]

sep_3()
riga_3("Payload inviato", "Byte osservati", "Esito atteso")
sep_3()

for i in range(len(chars)):
    payload = "COOKIE=" + chars[i]
    size    = misura(SECRET_5, payload)
    riga_3(payload, "%d byte" % size, esiti[i])

sep_3()
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()