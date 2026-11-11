import zlib

OUTPUT_FILE = "risultati_contromisure.txt"

SECRET       = "COOKIE=Sess42xK"
KNOWN_PREFIX = "COOKIE="
CHARSET      = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=_-"

class Server:
    def __init__(self, secret, compressione_attiva):
        self.secret             = secret
        self.compressione_attiva = compressione_attiva

    def comprimi_e_invia(self, messaggio):
        dato = self.secret + messaggio
        if self.compressione_attiva:
            return zlib.compress(dato, 6)
        else:
            return dato

class Client:
    def __init__(self, nome):
        self.nome = nome

    def invia(self, server, messaggio):
        return server.comprimi_e_invia(messaggio)

class Attaccante:
    def __init__(self, server, prefisso_noto):
        self.server        = server
        self.prefisso_noto = prefisso_noto
        self.scoperto      = ""

    def inietta(self, carattere):
        payload   = self.prefisso_noto + self.scoperto + carattere
        pacchetto = self.server.comprimi_e_invia(payload)
        return len(pacchetto)

    def scopri_carattere(self):
        min_size  = 99999
        best_char = "?"

        for char in CHARSET:
            dim = self.inietta(char)
            if dim < min_size:
                min_size  = dim
                best_char = char

        self.scoperto += best_char
        return best_char, min_size

    def segnale_rilevabile(self):
        secret_suffix = SECRET[len(KNOWN_PREFIX):]
        correct_char  = secret_suffix[0]
        size_match    = self.inietta(correct_char)
        size_mismatch = self.inietta("Z")
        return size_mismatch - size_match

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def sep_com():
    scrivi("+" + "-"*27 + "+" + "-"*22 + "+" + "-"*18 + "+")

def riga_com(col1, col2, col3):
    scrivi("| %-25s | %-20s | %-16s |" % (col1, col2, col3))

def sep_att():
    scrivi("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*12 + "+")

def riga_att(col1, col2, col3, col4):
    scrivi("| %-10s | %-14s | %-14s | %-10s |" % (col1, col2, col3, col4))

def sep_confronto():
    scrivi("+" + "-"*42 + "+" + "-"*18 + "+" + "-"*18 + "+")

def riga_confronto(col1, col2, col3):
    scrivi("| %-40s | %-16s | %-16s |" % (col1, col2, col3))


def simula_scenario(titolo, compressione_attiva, f_obj):
    server     = Server(SECRET, compressione_attiva)
    client     = Client("Client legittimo")
    attaccante = Attaccante(server, KNOWN_PREFIX)

    stato = "ATTIVA" if compressione_attiva else "DISABILITATA"

    scrivi("")
    scrivi("="*70)
    scrivi("      %s - Compressione %s" % (titolo, stato))
    scrivi("="*70)
    scrivi("")

    messaggi_legittimi = [
        "Ciao server, come stai?",
        "Voglio accedere alla mia area riservata.",
        "Grazie, a presto."
    ]

    scrivi(">> COMUNICAZIONE LEGITTIMA")
    scrivi("-" * 70)
    sep_com()
    riga_com("Messaggio del client", "Dim. pacchetto", "Attaccante")
    sep_com()

    for messaggio in messaggi_legittimi:
        pacchetto     = client.invia(server, messaggio)
        dim_pacchetto = len(pacchetto)
        riga_com(
            messaggio[:25],
            "%d byte (cifrato)" % dim_pacchetto,
            "osserva (%d byte)" % dim_pacchetto
        )

    sep_com()
    scrivi("")

    scrivi(">> INIEZIONE SILENZIOSA DELL'ATTACCANTE")
    scrivi("-" * 70)

    secret_suffix = SECRET[len(KNOWN_PREFIX):]
    correct       = 0
    total         = 0
    segnale       = attaccante.segnale_rilevabile()

    scrivi("  Segnale rilevato (match - mismatch): %d byte" % segnale)
    scrivi("")

    if segnale == 0:
        scrivi("  Segnale nullo: la compressione e' disabilitata.")
        scrivi("  L'attaccante non riesce a distinguere un carattere")
        scrivi("  corretto da uno sbagliato. Attacco impossibile.")
        scrivi("")
    else:
        sep_att()
        riga_att("Posizione", "Char trovato", "Dim. minima", "Corretto?")
        sep_att()

        for pos in range(len(secret_suffix)):
            real_char           = secret_suffix[pos]
            best_char, min_size = attaccante.scopri_carattere()
            total              += len(CHARSET)

            ok = (best_char == real_char)
            if ok:
                correct += 1

            riga_att(
                "Pos. %d" % (pos + 1),
                "'%s'" % best_char,
                "%d byte" % min_size,
                "SI'" if ok else "NO"
            )

            client.invia(server, "Messaggio legittimo %d" % (pos + 1))

        sep_att()
        scrivi("")
        accuratezza = correct * 100 / len(secret_suffix)
        scrivi("  Segreto reale:       " + SECRET)
        scrivi("  Segreto ricostruito: " + KNOWN_PREFIX + attaccante.scoperto)
        scrivi("  Accuratezza:         %d%%" % accuratezza)
        scrivi("  Tentativi totali:    %d" % total)

    scrivi("")
    return segnale, correct, len(secret_suffix)

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      CONTROMISURE - Confronto con e senza compressione")
scrivi("="*70)
scrivi("")
scrivi("  Questo script dimostra perche' la disabilitazione della")
scrivi("  compressione TLS e' l'unica contromisura efficace contro CRIME.")
scrivi("  Lo stesso attacco MitM silenzioso viene eseguito due volte:")
scrivi("  prima con compressione attiva, poi con compressione disabilitata.")
scrivi("")

segnale1, correct1, total_pos = simula_scenario(
    "SCENARIO 1", True, f
)

segnale2, correct2, _ = simula_scenario(
    "SCENARIO 2", False, f
)

scrivi("")
scrivi("="*70)
scrivi("      CONFRONTO FINALE")
scrivi("="*70)
scrivi("")

sep_confronto()
riga_confronto("Parametro", "CON compressione", "SENZA compressione")
sep_confronto()
riga_confronto("Segnale rilevato (byte)", "%d byte" % segnale1, "%d byte" % segnale2)
riga_confronto("Caratteri scoperti", "%d / %d" % (correct1, total_pos), "0 / %d" % total_pos)
riga_confronto("Attacco riuscito?", "SI' (parzialmente)", "NO")
riga_confronto("Comunicazione legittima", "Ininterrotta", "Ininterrotta")
sep_confronto()

scrivi("")
scrivi("  La disabilitazione della compressione azzera completamente")
scrivi("  il segnale su cui si basa CRIME. La comunicazione legittima")
scrivi("  tra client e server non viene influenzata in alcun modo.")
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()