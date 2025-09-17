# Calcolatore di Processo per Stampaggio a Imbutitura

Questo progetto fornisce una suite di strumenti a riga di comando per la progettazione e l'analisi di processi di stampaggio a imbutitura profonda.

Il software è organizzato in due moduli principali, a seconda della geometria del pezzo:
- **`cilindrico/`**: Contiene gli strumenti per la progettazione e l'analisi di pezzi a base circolare.
- **`rettangolare/`**: Contiene lo strumento avanzato per la progettazione di pezzi a base rettangolare.

---

## Strumenti per Pezzi CILINDRICI (`cilindrico/`)

Per i pezzi cilindrici sono disponibili due strumenti distinti.

### 1. Progettare un Nuovo Processo (`progetta_processo.py`)

Da usare quando si parte da zero per definire una sequenza di stampaggio sicura.

1.  **Configura i parametri:** Apri il file `cilindrico/progetto_imbutitura.csv` e inserisci i dati del pezzo finale e i rapporti limite di imbutitura (LDR) desiderati.
2.  **Esegui lo script:**
    ```bash
    python cilindrico/progetta_processo.py
    ```
3.  **Risultato:** Lo script propone una sequenza di passaggi e la valida, analizzando forze e deformazioni.

### 2. Analizzare un Processo Esistente (`analizza_processo.py`)

Da usare per verificare un processo già in uso o per simulare variazioni su di esso.

1.  **Configura i parametri:** Apri `cilindrico/parametri_imbutitura.csv` e inserisci la sequenza esatta dei diametri dei punzoni utilizzati.
2.  **Esegui lo script:**
    ```bash
    python cilindrico/analizza_processo.py
    ```
3.  **Risultato:** Lo script simula il processo passo-passo e fornisce un report dettagliato su tensioni e forze.

---

## Strumento per Pezzi RETTANGOLARI (`rettangolare/`)

Per i pezzi rettangolari è disponibile un unico strumento di **progettazione intelligente**, ideale per la preventivazione.

### Progettare un Processo Ottimale (`progetta_processo_rettangolare.py`)

Questo script determina automaticamente se è necessario uno o due passaggi e progetta la soluzione più sicura ed economica.

1.  **Configura i parametri:** Apri `rettangolare/progetto_rettangolare.csv` e inserisci le dimensioni e le caratteristiche del **pezzo finale**.
2.  **Esegui lo script:**
    ```bash
    python rettangolare/progetta_processo_rettangolare.py
    ```
3.  **Analisi Automatica:** Lo script esegue la seguente logica:
    *   **Tenta un passaggio singolo:** Valuta se il pezzo è realizzabile in un colpo solo, controllando che la deformazione del materiale non superi una soglia di sicurezza (impostata all'84%).
    *   **Progetta due passaggi (se necessario):** Se il passaggio singolo è troppo rischioso, lo script **progetta automaticamente uno stampo intermedio** e ne calcola le dimensioni (altezza, raggi, ecc.).
    *   **Valida la soluzione:** Verifica che entrambi i passaggi della nuova soluzione siano sicuri, sia per il materiale che per la pressa.

4.  **Risultato:** Lo script ti fornisce una **soluzione concreta e validata**, indicandoti se procedere con uno o due stampi e, nel secondo caso, fornendoti le specifiche di massima per il primo passaggio.

---

## Requisiti

Assicurarsi di avere installato le librerie necessarie:

```bash
pip install -r requirements.txt
```
