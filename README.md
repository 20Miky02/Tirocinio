# Tirocinio — Studio e Testing dell'attacco CRIME a TLS

Questa repository raccoglie il lavoro svolto durante il mio
periodo di tirocinio, dedicato allo studio e alla simulazione
pratica dell'attacco CRIME (*Compression Ratio Info-leak Made
Easy*), una vulnerabilità del protocollo TLS scoperta nel
2012 che sfrutta la compressione dei dati come canale laterale
per ricostruire informazioni riservate, come i cookie di
sessione, senza violare la cifratura.

Il progetto si articola in diverse fasi di studio: una fase
teorica iniziale dedicata alla comprensione e conoscenza del
protocollo TLS e dell'attacco CRIME; successivamente una
fase pratica, svolta su macchina Debian con OPENSSL
vulnerabile, dove sono stati prodotti differenti script
Python per riprodurre il meccanismo dell'attacco in modo
progressivo - dall'osservazione del comportamento della
compressione fino alla ricostruzione automatica di un segreto;
infine una simulazione più realistica con tre processi
separati (server, client e attaccante) che comunicano tramite
socket, a riprodurre un attacco Man-in-the-Middle silenzioso.

Il lavoro è stato svolto come parte del mio percorso di
tirocinio ed elaborato finale triennale, con l'obiettivo di
comprendere a fondo il funzionamento dell'attacco e 
dimostrarne concretamente i meccanismi e le contromisure.