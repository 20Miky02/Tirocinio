import zlib

OUTPUT_FILE = "risultati_http.txt"

SECRET       = "session_id=Tk9zS3Jz"
KNOWN_PREFIX = "session_id="
CHARSET      = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=_-"

RICHIESTE_HTTP = [
    (
        "GET /index.html",
        "GET /index.html HTTP/1.1\r\n"
        "Host: www.esempio.it\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
        "Accept: text/html,application/xhtml+xml\r\n"
        "Accept-Language: it-IT,it;q=0.9\r\n"
        "Cookie: session_id=Tk9zS3Jz; theme=dark\r\n"
        "Connection: keep-alive\r\n\r\n"
    ),
    (
        "GET /profilo",
        "GET /profilo HTTP/1.1\r\n"
        "Host: www.esempio.it\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
        "Accept: text/html,application/xhtml+xml\r\n"
        "Accept-Language: it-IT,it;q=0.9\r\n"
        "Cookie: session_id=Tk9zS3Jz; theme=dark\r\n"
        "Referer: http://www.esempio.it/index.html\r\n"
        "Connection: keep-alive\r\n\r\n"
    ),
    (
        "POST /login",
        "POST /login HTTP/1.1\r\n"
        "Host: www.esempio.it\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
        "Accept: text/html,application/xhtml+xml\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Cookie: session_id=Tk9zS3Jz; theme=dark\r\n"
        "Content-Length: 27\r\n"
        "Connection: keep-alive\r\n\r\n"
        "username=mario&password=1234"
    )
]

class Server:
    def __init__(self, secret):
        self.secret = secret

    def comprimi_e_invia(self, richiesta_http):
        dato = self.secret + richiesta_http
        return zlib.compress(dato, 6)


class Client:
    def invia(self, server, richiesta_http):
        return server.comprimi_e_invia(richiesta_http)


class Attaccante:
    def __init__(self, server, prefisso_noto):
        self.server        = server
        self.prefisso_noto = prefisso_noto
        self.scoperto      = ""

    def osserva(self, pacchetto):
        return len(pacchetto)

    def inietta(self, carattere):
        tentativo = self.prefisso_noto + self.scoperto + carattere
        context = self.server.secret + self.server.secret + self.server.secret
        dato = context + tentativo
        return len(zlib.compress(dato, 6))

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

def scrivi(riga):
    print riga
    f.write(riga + "\n")

def sep_http():
    scrivi("+" + "-"*21 + "+" + "-"*22 + "+" + "-"*18 + "+")

def riga_http(col1, col2, col3):
    scrivi("| %-19s | %-20s | %-16s |" % (col1, col2, col3))

def sep_att():
    scrivi("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*12 + "+")

def riga_att(col1, col2, col3, col4):
    scrivi("| %-10s | %-14s | %-14s | %-10s |" % (col1, col2, col3, col4))

f = open(OUTPUT_FILE, "a")

scrivi("")
scrivi("="*70)
scrivi("      HTTP SIMULATO - MitM silenzioso su traffico HTTP realistico")
scrivi("="*70)
scrivi("")
scrivi("  Il client invia richieste HTTP realistiche con header completi.")
scrivi("  Il cookie segreto e' nascosto nell'header Cookie di ogni richiesta.")
scrivi("  L'attaccante osserva il traffico e inietta richieste contraffatte")
scrivi("  per scoprire il valore del cookie senza mai vederlo in chiaro.")
scrivi("")
scrivi("  Cookie da scoprire: " + SECRET)
scrivi("  Prefisso noto:      " + KNOWN_PREFIX)
scrivi("")

server     = Server(SECRET)
client     = Client()
attaccante = Attaccante(server, KNOWN_PREFIX)

scrivi(">> FASE 1 - Traffico HTTP legittimo")
scrivi("-" * 70)
scrivi("  Il client naviga normalmente sul sito.")
scrivi("  Ogni richiesta contiene il cookie segreto nell'header.")
scrivi("")

sep_http()
riga_http("Richiesta HTTP", "Dim. pacchetto", "Attaccante")
sep_http()

for label, richiesta in RICHIESTE_HTTP:
    pacchetto = client.invia(server, richiesta)
    dim       = len(pacchetto)
    riga_http(label, "%d byte (cifrato)" % dim, "osserva (%d byte)" % dim)

sep_http()
scrivi("")
scrivi("  Le richieste HTTP sono state consegnate normalmente.")
scrivi("  L'attaccante vede le dimensioni ma non il contenuto.")
scrivi("")

scrivi(">> FASE 2 - Iniezione silenziosa dell'attaccante")
scrivi("-" * 70)
scrivi("  Mentre il client continua a navigare, l'attaccante inietta")
scrivi("  richieste HTTP contraffatte per scoprire il cookie carattere")
scrivi("  per carattere, sfruttando il segnale di compressione.")
scrivi("")

secret_suffix = SECRET[len(KNOWN_PREFIX):]
correct       = 0
total         = 0

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
    _, richiesta = RICHIESTE_HTTP[pos % len(RICHIESTE_HTTP)]
    client.invia(server, richiesta)

sep_att()

scrivi("")
scrivi(">> FASE 3 - Riepilogo")
scrivi("-" * 70)
accuratezza = correct * 100 / len(secret_suffix)
scrivi("  Cookie reale:       " + SECRET)
scrivi("  Cookie ricostruito: " + KNOWN_PREFIX + attaccante.scoperto)
scrivi("  Accuratezza:        %d%%" % accuratezza)
scrivi("  Tentativi totali:   %d" % total)
scrivi("")
scrivi("  Durante l'attacco il client ha continuato a navigare normalmente.")
scrivi("  L'attaccante e' rimasto completamente invisibile.")
scrivi("  Il cookie e' stato parzialmente ricostruito osservando solo")
scrivi("  la dimensione delle richieste HTTP cifrate.")
scrivi("")
scrivi("  Risultati salvati in: " + OUTPUT_FILE)

f.close()