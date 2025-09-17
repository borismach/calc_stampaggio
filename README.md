# calc_stampaggio
Calcolatore per processo di stampaggio a freddo

## Descrizione
Questo script Python calcola i parametri chiave per un processo di imbutitura profonda, tra cui:
* Il diametro del disco iniziale (blank).
* Il numero di passaggi di imbutitura necessari.
* I diametri dei punzoni per ogni passaggio.
* La forza di imbutitura e la forza del premilamiera per ogni passaggio.

I calcoli si basano sui parametri forniti in un file `parametri_imbutitura.csv`.

## Prerequisiti
Assicurati di avere Python installato. L'unica dipendenza esterna è la libreria `pandas`. Puoi installarla con pip:
```bash
pip install pandas
```
In alternativa, puoi utilizzare il file `requirements.txt` fornito:
```bash
pip install -r requirements.txt
```

## Guida all'utilizzo

### 1. Configura i parametri di input
Modifica il file `parametri_imbutitura.csv` per definire le specifiche del tuo pezzo e del tuo materiale. Assicurati che il file sia nella stessa directory dello script `calc_stamp.py`.

Il file CSV deve contenere le seguenti colonne: `parametro`, `valore`, `unita_misura`, `descrizione`.

I parametri da configurare sono:

| parametro | valore | unità_misura | descrizione |
|---|---|---|---|
| diametro_finale_cilindro | 50.0 | mm | Diametro esterno del cilindro finito |
| altezza_finale_cilindro | 60.0 | mm | Altezza del cilindro finito |
| raggio_raccordo_fondo | 5.0 | mm | Raggio di raccordo tra fondo e parete del cilindro |
| spessore_lamiera | 1.0 | mm | Spessore della lamiera di partenza |
| ldr_primo_passaggio | 1.9 | | LDR massimo per il primo passaggio (es. 1.8-2.0) |
| ldr_passaggi_successivi | 1.25 | | LDR massimo per i passaggi successivi (es. 1.15-1.30) |
| resistenza_trazione_Rm | 600 | MPa | Resistenza a trazione del materiale (dal certificato 3.1) |
| limite_snervamento_Rp02 | 280 | MPa | Limite di snervamento del materiale (dal certificato 3.1) |
| forza_max_pressa | 1000 | kN | Forza massima della pressa idraulica |
| pressione_premilamiera | 2.0 | N/mm^2 | Pressione specifica del cuscino premilamiera |

### 2. Esegui lo script
Una volta configurati i parametri, esegui lo script dalla riga di comando:
```bash
python calc_stamp.py
```

### 3. Analizza i risultati
Lo script stamperà a schermo i seguenti risultati:
* **Diametro iniziale del disco (D0):** Il diametro del disco di lamiera da cui partire.
* **Numero totale stimato di passaggi:** Quanti step di imbutitura sono necessari.
* **Diametri dei punzoni suggeriti:** Una lista dei diametri dei punzoni da utilizzare per ogni passaggio.
* **Analisi Forze per Passaggio:** Per ogni passaggio, verranno stimate:
    * La **Forza di Imbutitura** in kN.
    * La **Forza Premilamiera** in kN.
    * Un **avviso** se la forza combinata supera la forza massima della pressa specificata.

## Esempio di output
```
--- Inizio Calcoli Imbutitura ---
Parametri caricati: {'diametro_finale_cilindro': 50.0, ...}

Diametro iniziale del disco (D0): 123.45 mm

Passaggio 1: Diametro punzone = 65.00 mm
Passaggio 2: Diametro punzone = 52.00 mm
...

Numero totale stimato di passaggi di imbutitura: 2
Diametri dei punzoni suggeriti per ogni passaggio: 65.00, 52.00 mm

--- Analisi Forze per Passaggio ---
Passaggio 1 (Punzone Ø 65.00 mm):
  Forza di Imbutitura stimata: 280.00 kN
  Forza Premilamiera stimata: 150.00 kN
Passaggio 2 (Punzone Ø 52.00 mm):
  Forza di Imbutitura stimata: 220.00 kN
  Forza Premilamiera stimata: 80.00 kN
  ATTENZIONE: La forza combinata (300.00 kN) supera la forza massima della pressa (250.00 kN)!

--- Fine Calcoli Imbutitura ---
```
