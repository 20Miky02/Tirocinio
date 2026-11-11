SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999
MITM_PORT   = 9998
SECRET       = "session_id=Tk9zS3Jz"
KNOWN_PREFIX = "session_id="
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=_-"

OUTPUT_FILE = "risultati_processi.txt"

RICHIESTE_HTTP = [
    "GET /index.html HTTP/1.1\r\nHost: www.esempio.it\r\nCookie: session_id=Tk9zS3Jz; theme=dark\r\n\r\n",
    "GET /profilo HTTP/1.1\r\nHost: www.esempio.it\r\nCookie: session_id=Tk9zS3Jz; theme=dark\r\n\r\n",
    "POST /login HTTP/1.1\r\nHost: www.esempio.it\r\nCookie: session_id=Tk9zS3Jz\r\nContent-Length: 27\r\n\r\nusername=mario&password=1234"
]