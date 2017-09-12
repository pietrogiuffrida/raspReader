# raspReader

Codice python per configurare i pin **gpio** del **raspberry py** in modalità input e monitorarne lo stato in modo continuativo.

Il codice permette anche di tenere un *log* delle commutazioni di stato, sia in un file di testo, sia in un'istanza di mongoDB.

A seconda degli eventi, è possibile configurare l'invio automatico di email per evidenziare ad un gruppo di recipients gli eventi registrati.

La configurazione dei pin e delle azioni da scatenare caso per caso si trova nel file di configurazione.
