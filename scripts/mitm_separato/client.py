import socket
import time
from config import SERVER_HOST, SERVER_PORT, MITM_PORT, RICHIESTE_HTTP, OUTPUT_FILE

def avvia_client(usa_mitm=False):
    host = SERVER_HOST
    port = MITM_PORT if usa_mitm else SERVER_PORT

    print "[CLIENT] Avviato. Connessione a %s:%d" % (host, port)
    time.sleep(0.5)

    f = open(OUTPUT_FILE, "a")
    f.write("\n")
    f.write("="*70 +"\n")
    if usa_mitm:
        f.write("      COMUNICAZIONE CLIENT - tramite MitM\n")
    else:
        f.write("      COMUNICAZIONE CLIENT - diretta al server\n")
    f.write("="*70 + "\n\n")
    f.write("+" + "-"*22 + "+" + "-"*24 + "+" + "-"*18 + "+\n")
    f.write("| %-20s | %-22s | %-16s |\n" % ("Richiesta HTTP", "Dim. pacchetto server", "Stato"))
    f.write("+" + "-"*22 + "+" + "-"*24 + "+" + "-"*18 + "+\n")

    for i, richiesta in enumerate(RICHIESTE_HTTP):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(richiesta)
            risposta = s.recv(1024)
            s.close()

            label = richiesta.split("\r\n")[0][:20]
            riga  = "| %-20s | %-22s | %-16s |\n" % (label, risposta + " byte", "Consegnata")
            f.write(riga)
            print riga.strip()
            print "[CLIENT] Richiesta %d inviata -> risposta: %s byte" % (i+1, risposta)
            time.sleep(0.3)

        except Exception as e:
            print "[CLIENT] Errore: %s" % str(e)

    f.write("+" + "-"*22 + "+" + "-"*24 + "+" + "-"*18 + "+\n\n")
    f.write("  Il client ha completato tutte le richieste.\n\n")
    f.close()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_HOST, SERVER_PORT))
        s.send("STOP")
        s.close()
    except:
        pass

    print "[CLIENT] Completato."

if __name__ == "__main__":
    avvia_client(usa_mitm=False)