import zlib
import socket
from config import SERVER_HOST, SERVER_PORT, MITM_PORT, SECRET, KNOWN_PREFIX, CHARSET, RICHIESTE_HTTP, OUTPUT_FILE

def esegui_iniezioni():
    secret_suffix = SECRET[len(KNOWN_PREFIX):]
    scoperto      = ""
    iniezioni     = []

    print "[MITM] Inizio iniezioni silenziose..."

    for pos in range(len(secret_suffix)):
        min_size  = 99999
        best_char = "?"

        for char in CHARSET:
            tentativo  = KNOWN_PREFIX + scoperto + char
            context    = SECRET + SECRET + SECRET
            compressed = zlib.compress(context + tentativo, 6)
            dim        = len(compressed)
            if dim < min_size:
                min_size  = dim
                best_char = char

        real_char = secret_suffix[pos]
        ok        = (best_char == real_char)
        scoperto += best_char
        iniezioni.append((pos + 1, best_char, min_size, ok))

        print "[MITM] Pos. %d -> char trovato: '%s' (%s)" % (
            pos + 1, best_char, "corretto" if ok else "errato"
        )

    return scoperto, iniezioni

def gestisci_traffico():
    print "[MITM] In ascolto su %s:%d" % (SERVER_HOST, MITM_PORT)

    mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mitm_socket.bind((SERVER_HOST, MITM_PORT))
    mitm_socket.listen(5)

    richieste_ricevute = 0

    while richieste_ricevute < len(RICHIESTE_HTTP):
        try:
            mitm_socket.settimeout(30)
            conn, addr = mitm_socket.accept()
            dati = conn.recv(4096)

            if not dati:
                conn.close()
                continue

            server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_conn.connect((SERVER_HOST, SERVER_PORT))
            server_conn.send(dati)
            risposta = server_conn.recv(1024)
            server_conn.close()

            conn.send(risposta)
            conn.close()

            print "[MITM] Richiesta intercettata -> dim. pacchetto: %s byte" % risposta
            richieste_ricevute += 1

        except socket.timeout:
            break
        except Exception as e:
            print "[MITM] Errore: %s" % str(e)
            break

    mitm_socket.close()
    return richieste_ricevute

def avvia_mitm():
    print "[MITM] Avviato su %s:%d" % (SERVER_HOST, MITM_PORT)
    print "[MITM] Inoltro verso server %s:%d" % (SERVER_HOST, SERVER_PORT)

    f = open(OUTPUT_FILE, "a")
    f.write("\n")
    f.write("="*70 + "\n")
    f.write("      ATTACCANTE MitM - Osservazione e iniezione silenziosa\n")
    f.write("=" + "\n\n")

    scoperto, iniezioni = esegui_iniezioni()

    print "[MITM] Iniezioni completate. Ora gestisco il traffico del client..."
    richieste_ricevute = gestisci_traffico()

    correct = sum(1 for _, _, _, ok in iniezioni if ok)

    f.write(">> INIEZIONI SILENZIOSE EFFETTUATE\n")
    f.write("-" * 70 + "\n")
    f.write("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*18 + "+" + "-"*12 + "+\n")
    f.write("| %-10s | %-14s | %-16s | %-10s |\n" % (
        "Posizione", "Char trovato", "Dim. minima", "Corretto?"))
    f.write("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*18 + "+" + "-"*12 + "+\n")

    for pos, char, dim, ok in iniezioni:
        f.write("| %-10s | %-14s | %-16s | %-10s |\n" % (
            "Pos. %d" % pos,
            "'%s'" % char,
            "%d byte" % dim,
            "SI'" if ok else "NO"
        ))

    f.write("+" + "-"*12 + "+" + "-"*16 + "+" + "-"*18 + "+" + "-"*12 + "+\n\n")
    f.write("  Segreto reale:            %s\n" % SECRET)
    f.write("  Segreto ricostruito:      %s%s\n" % (KNOWN_PREFIX, scoperto))
    if len(iniezioni) > 0:
        f.write("  Accuratezza:             %d%%\n" % (correct * 100 / len(iniezioni)))
    f.write("  Iniezioni totali:         %d\n" % len(iniezioni))
    f.write("  Richieste client gestite: %d\n" % richieste_ricevute)
    f.write("\n  Risultati salvati in: %s\n" % OUTPUT_FILE)
    f.close()

    print "[MITM] Completato."

if __name__ == "__main__":
    avvia_mitm()