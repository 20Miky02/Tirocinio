import zlib
import socket
from config import SERVER_HOST, SERVER_PORT, SECRET, OUTPUT_FILE

def avvia_server():
    print "[SERVER] Avviato su %s:%d" % (SERVER_HOST, SERVER_PORT)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    while True:
        try:
            conn, addr = server_socket.accept()
            dati = conn.recv(4096)

            if not dati:
                conn.close()
                continue

            if dati == "STOP":
                print "[SERVER] Segnale di stop ricevuto. Chiusura."
                conn.close()
                break

            compressed = zlib.compress(SECRET + dati, 6)
            dim        = str(len(compressed))

            print "[SERVER] Richiesta ricevuta (%d byte) -> compressa: %s byte" % (len(dati), dim)
            conn.send(dim)
            conn.close()

        except Exception as e:
            print "[SERVER] Errore: %s" % str(e)
            break

    server_socket.close()
    print "[SERVER] Chiuso."

if __name__ == "__main__":
    avvia_server()