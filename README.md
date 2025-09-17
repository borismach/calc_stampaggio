# Calcolatore di Processo per Stampaggio a Imbutitura

Questo progetto fornisce una suite di strumenti a riga di comando per la progettazione e l'analisi di processi di stampaggio a imbutitura profonda per la produzione di componenti cilindrici.

## Funzionalità Principali

- **Progettazione di Processo (`progetta_processo.py`):** Genera una sequenza di passaggi di imbutitura ottimale basandosi sulle dimensioni finali del pezzo e sulle proprietà del materiale.
- **Analisi di Processo (`analizza_processo.py`):** Simula un processo di imbutitura esistente con una sequenza di passaggi definita dall'utente per valutarne la fattibilità.
- **Simulazione Fisica:** Entrambi gli script includono un modello di simulazione che calcola:
  - L'incrudimento del materiale ad ogni passaggio.
  - La tensione di imbutitura e il rischio di rottura del materiale.
  - Le forze di imbutitura e del premilamiera necessarie.
- **Validazione Macchina:** Verifica che le forze calcolate non superino i limiti massimi della pressa e del cuscino premilamiera.

---

## Come Utilizzare

Il software è diviso in due script principali, a seconda dell'obiettivo.

### 1. Progettare un Nuovo Processo (`progetta_processo.py`)

Da usare quando si parte da zero e si vuole definire una sequenza di stampaggio sicura.

1.  **Configura i parametri:** Apri il file `progetto_imbutitura.csv` e inserisci i dati richiesti:
    *   Dimensioni finali del pezzo (diametro, altezza, raggio di raccordo).
    *   Proprietà del materiale (spessore, Rm, Rp02, coefficiente di incrudimento n).
    *   Rapporti limite di imbutitura (LDR) per il primo passaggio e per i successivi.
    *   Limiti della macchina (forza massima della pressa e del cuscino).

2.  **Esegui lo script:**
    ```bash
    python progetta_processo.py
    ```

3.  **Analizza i risultati:** Lo script calcolerà il diametro del disco di partenza e proporrà una sequenza di punzoni. Successivamente, validerà il processo e stamperà un'analisi dettagliata per ogni passaggio, evidenziando eventuali rischi di rottura o superamento dei limiti della macchina.

### 2. Analizzare un Processo Esistente (`analizza_processo.py`)

Da usare per verificare un processo già in uso in officina o per simulare variazioni su di esso.

1.  **Configura i parametri:** Apri il file `parametri_imbutitura.csv` e inserisci i dati:
    *   La **sequenza esatta dei diametri dei punzoni** utilizzati, separati da virgola.
    *   Le stesse informazioni su materiale e macchina richieste per la progettazione.
    *   Il diametro reale del disco di partenza utilizzato.

2.  **Esegui lo script:**
    ```bash
    python analizza_processo.py
    ```

3.  **Analizza i risultati:** Lo script simulerà il processo passo dopo passo e fornirà un report dettagliato sulle tensioni e le forze generate, avvisando in caso di criticità.

---

## Dettagli Tecnici

Il calcolo del diametro del disco si basa su formule geometriche standard. La simulazione del processo implementa la legge di Hollomon per modellare l'incrudimento del materiale (`σ = K * ε^n`) e stima le tensioni e le forze basandosi su principi di ingegneria dei processi di formatura.

## Requisiti

Assicurarsi di avere installato le librerie necessarie:

```bash
pip install -r requirements.txt
```
