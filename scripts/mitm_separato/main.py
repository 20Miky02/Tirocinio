import multiprocessing
import time
from config import OUTPUT_FILE
from server import avvia_server
from client import avvia_client
from mitm import avvia_mitm

if __name__ == "__main__":
    f = open(OUTPUT_FILE, "w")
    f.write("SIMULAZIONE MitM CON PROCESSI SEPARATI\n")
    f.write("=" * 70 + "\n\n")
    f.close()

    print
    ""
    print
    "=" * 70
    print
    "  FASE 1 - Server e Client (comunicazione diretta, senza MitM)"
    print
    "=" * 70
    print
    ""

    p_server = multiprocessing.Process(target=avvia_server)
    p_server.start()
    time.sleep(0.5)

    p_client = multiprocessing.Process(target=avvia_client, args=(False,))
    p_client.start()

    p_client.join()
    p_server.join(timeout=3)
    if p_server.is_alive():
        p_server.terminate()

    print
    ""
    print
    "  Fase 1 completata."
    print
    ""
    time.sleep(1)

    print
    "=" * 70
    print
    "  FASE 2 - Server + MitM + Client (attacco completo)"
    print
    "=" * 70
    print
    ""

    p_server2 = multiprocessing.Process(target=avvia_server)
    p_server2.start()
    time.sleep(0.5)

    p_mitm = multiprocessing.Process(target=avvia_mitm)
    p_mitm.start()

    print
    "  [MAIN] Attendo che il MitM completi le iniezioni..."
    time.sleep(8)

    p_client2 = multiprocessing.Process(target=avvia_client, args=(True,))
    p_client2.start()

    p_client2.join()
    p_mitm.join(timeout=15)
    if p_mitm.is_alive():
        p_mitm.terminate()
    p_server2.join(timeout=3)
    if p_server2.is_alive():
        p_server2.terminate()

    print
    ""
    print
    "=" * 70
    print
    "  Simulazione completata! Risultati in: " + OUTPUT_FILE
    print
    "=" * 70