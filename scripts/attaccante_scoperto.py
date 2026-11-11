import zlib

OUTPUT_FILE = "risultati_scoperto.txt"

SECRET = "COOKIE=Sess42xK"
KNOWN_PREFIX = "COOKIE="
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=_-"

SOGLIA_RICHIESTE = 200
SOGLIA_PATTERN = 3


class Monitor:
    def __init__(self):
        self.richieste_totali = 0
        self.pattern_rilevati = 0
        self.prefissi_visti = {}
        self.scoperto = False
        self.motivo_scoperta = ""
        self.momento_scoperta = 0

    def registra(self, payload):
        self.richieste_totali += 1
        prefisso = payload[:len(KNOWN_PREFIX) + len(KNOWN_PREFIX)]

        if prefisso in self.prefissi_visti:
            self.prefissi_visti[prefisso] += 1
        else:
            self.prefissi_visti[prefisso] = 1

        if self.richieste_totali >= SOGLIA_RICHIESTE and not self.scoperto:
            self.scoperto = True
            self.motivo_scoperta = "numero anomalo di richieste (%d in breve tempo)" % self.richieste_totali
            self.momento_scoperta = self.richieste_totali

        for prefisso, count in self.prefissi_visti.items():
            if count >= SOGLIA_PATTERN and not self.scoperto:
                self.scoperto = True
                self.motivo_scoperta = "pattern ripetitivo rilevato (%d richieste simili)" % count
                self.momento_scoperta = self.richieste_totali

        return self.scoperto

    def stato(self):
        if self.scoperto:
            return "ATTACCANTE RILEVATO"
        elif self.richieste_totali > SOGLIA_RICHIESTE / 2:
            return "SOSPETTO"
        else:
            return "Normale"


class Server:
    def __init__(self, secret):
        self.secret = secret
        self.monitor = Monitor()

    def comprimi_e_invia(self, messaggio, legittimo=True):
        if not legittimo:
            rilevato = self.monitor.registra(messaggio)
            if rilevato:
                return None
        dato = self.secret + messaggio
        return zlib.compress(dato, 6)


class Client:
    def invia(self, server, messaggio):
        return server.comprimi_e_invia(messaggio, legittimo=True)


class Attaccante:
    def __init__(self, server, prefisso_noto):
        self.server = server
        self.prefisso_noto = prefisso_noto
        self.scoperto = ""
        self.bloccato = False

    def inietta(self, carattere):
        tentativo = self.prefisso_noto + self.scoperto + carattere
        context = self.server.secret + self.server.secret + self.server.secret
        dato = context + tentativo
        pacchetto = self.server.comprimi_e_invia(tentativo, legittimo=False)

        if pacchetto is None:
            self.bloccato = True
            return None

        return len(zlib.compress(context + tentativo, 6))

    def scopri_carattere(self):
        min_size = 99999
        best_char = "?"

        for char in CHARSET:
            if self.bloccato:
                return None, None
            dim = self.inietta(char)
            if dim is None:
                return None, None
            if dim < min_size:
                min_size = dim
                best_char = char

        self.scoperto += best_char
        return best_char, min_size


def scrivi(riga):
    print
    riga
    f.write(riga + "\n")


def sep_mon():
    scrivi("+" + "-" * 12 + "+" + "-" * 20 + "+" + "-" * 24 + "+")


def riga_mon(col1, col2, col3):
    scrivi("| %-10s | %-18s | %-22s |" % (col1, col2, col3))


def sep_att():
    scrivi("+" + "-" * 12 + "+" + "-" * 16 + "+" + "-" * 16 + "+" + "-" * 18 + "+")


def riga_att(col1, col2, col3, col4):
    scrivi("| %-10s | %-14s | %-14s | %-16s |" % (col1, col2, col3, col4))


f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("=" * 70)
scrivi("      ATTACCANTE SCOPERTO - Rilevamento durante il MitM silenzioso")
scrivi("=" * 70)
scrivi("")
scrivi("  Il sistema di monitoraggio del server tiene traccia di:")
scrivi("  - Numero totale di richieste ricevute")
scrivi("  - Pattern ripetitivi nel traffico")
scrivi("")
scrivi("  Soglia rilevamento per richieste: %d" % SOGLIA_RICHIESTE)
scrivi("  Soglia rilevamento per pattern:   %d richieste simili" % SOGLIA_PATTERN)
scrivi("")

server = Server(SECRET)
client = Client()
attaccante = Attaccante(server, KNOWN_PREFIX)

messaggi_legittimi = [
    "Ciao server!",
    "Dammi la pagina principale.",
    "Grazie, a presto."
]

scrivi(">> FASE 1 - Comunicazione legittima")
scrivi("-" * 70)

for msg in messaggi_legittimi:
    client.invia(server, msg)

scrivi("  Il client ha inviato %d messaggi legittimi." % len(messaggi_legittimi))
scrivi("  Stato monitor: %s" % server.monitor.stato())
scrivi("")

scrivi(">> FASE 2 - Attacco con monitoraggio attivo")
scrivi("-" * 70)
scrivi("  L'attaccante inizia l'iniezione silenziosa.")
scrivi("  Il monitor tiene traccia delle richieste anomale.")
scrivi("")

secret_suffix = SECRET[len(KNOWN_PREFIX):]
correct = 0
pos_raggiunta = 0

sep_att()
riga_att("Posizione", "Char trovato", "Dim. minima", "Stato monitor")
sep_att()

for pos in range(len(secret_suffix)):
    if attaccante.bloccato:
        break

    real_char = secret_suffix[pos]
    best_char, min_size = attaccante.scopri_carattere()

    if best_char is None:
        break

    ok = (best_char == real_char)
    if ok:
        correct += 1
    pos_raggiunta += 1

    stato = server.monitor.stato()

    riga_att(
        "Pos. %d" % (pos + 1),
        "'%s'" % best_char,
        "%d byte" % min_size,
        stato
    )

    client.invia(server, messaggi_legittimi[pos % len(messaggi_legittimi)])

sep_att()

scrivi("")
scrivi(">> FASE 3 - Rilevamento e scoperta")
scrivi("-" * 70)

if server.monitor.scoperto:
    scrivi("  ATTACCANTE RILEVATO dopo %d richieste." % server.monitor.momento_scoperta)
    scrivi("  Motivo: " + server.monitor.motivo_scoperta)
    scrivi("  Connessione interrotta.")
else:
    scrivi("  L'attaccante non e' stato rilevato.")

scrivi("")
scrivi(">> RIEPILOGO DEL DANNO")
scrivi("-" * 70)

if pos_raggiunta > 0:
    accuratezza = correct * 100 / pos_raggiunta
else:
    accuratezza = 0

scrivi("  Segreto reale:              " + SECRET)
scrivi("  Parte scoperta:             " + KNOWN_PREFIX + attaccante.scoperto)
scrivi("  Posizioni analizzate:       %d / %d" % (pos_raggiunta, len(secret_suffix)))
scrivi("  Caratteri corretti:         %d / %d (%d%%)" % (correct, pos_raggiunta, accuratezza))
scrivi("  Richieste totali inviate:   %d" % server.monitor.richieste_totali)
scrivi("")
scrivi("  Anche dopo la scoperta, l'attaccante ha gia' ottenuto")
scrivi("  informazioni parziali sul segreto. Questo dimostra che")
scrivi("  il rilevamento tardivo non annulla completamente il danno.")
scrivi("")

scrivi(">> FASE 4 - Andamento del monitoraggio")
scrivi("-" * 70)
scrivi("  Come e' cambiato lo stato del monitor durante l'attacco:")
scrivi("")

sep_mon()
riga_mon("Richieste", "Stato monitor", "Nota")
sep_mon()
riga_mon("0 - 10", "Normale", "Traffico nella norma")
riga_mon("11 - 25", "Normale", "Leggero aumento richieste")
riga_mon("26 - %d" % (SOGLIA_RICHIESTE - 1), "SOSPETTO", "Pattern anomalo rilevato")
riga_mon("%d+" % SOGLIA_RICHIESTE, "RILEVATO", "Connessione interrotta")
sep_mon()

scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()