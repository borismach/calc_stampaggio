import math
import pandas as pd

# --- Funzione di Calcolo Ausiliaria ---
def calcola_diametro_disco_iniziale(d_finale, h_finale, r_fondo):
    """Calcola il diametro teorico netto del disco di partenza."""
    if r_fondo == 0:
        return math.sqrt(d_finale ** 2 + 4 * d_finale * h_finale)
    return math.sqrt((d_finale - 2 * r_fondo) ** 2 + 4 * d_finale * (h_finale - r_fondo) + 
                     2 * math.pi * r_fondo * (d_finale - 0.7 * r_fondo))

# --- Main Script: Analista di Processo ---
if __name__ == "__main__":
    try:
        params = pd.read_csv('parametri_imbutitura.csv').set_index('parametro')['valore'].to_dict()

        print("--- Inizio Analisi di Processo Esistente (con Incrudimento) ---")

        # Caricamento parametri dal CSV
        d_finale = params['diametro_finale_cilindro']
        h_finale = params['altezza_finale_cilindro']
        r_fondo_finale = params['raggio_raccordo_fondo']
        r_punzone_intermedio = params['raggio_punzone_intermedio_mm']
        spessore = params['spessore_lamiera']
        rm_iniziale = params['resistenza_trazione_Rm']
        rp02_iniziale = params['limite_snervamento_Rp02']
        n_incrudimento = params['coefficiente_incrudimento_n']
        pressione_target = params['pressione_premilamiera_target_N_mm2']
        forza_max_pressa_N = params['forza_max_pressa'] * 1000
        forza_max_cuscino_N = params['forza_max_cuscino_kN'] * 1000
        soglia_sicurezza = 0.95 # Soglia di allarme per la rottura

        # Lettura della sequenza di passaggi dal CSV
        sequenza_str = params.get('sequenza_diametri_punzoni_mm')
        if not sequenza_str:
            raise ValueError("Il parametro 'sequenza_diametri_punzoni_mm' non è stato trovato nel CSV.")
        passi_da_simulare = [float(d.strip()) for d in sequenza_str.split(',')]

        # Calcolo e stampa del diametro teorico per riferimento
        d0_teorico = calcola_diametro_disco_iniziale(d_finale, h_finale, r_fondo_finale)
        print(f"\nDiametro teorico del disco (D0): {d0_teorico:.2f} mm (calcolo netto, non include flangia)")
        
        # Per la simulazione usiamo il diametro reale del disco
        d0_simulazione = 311.0 # Valore reale dall'officina
        print(f"Diametro disco usato per la simulazione: {d0_simulazione:.2f} mm (valore reale officina)")

        print(f"\nAnalisi di un processo a {len(passi_da_simulare)} passaggi basato sulla sequenza fornita...")
        print("--- Inizio Analisi Dettagliata ---")

        # Esecuzione della simulazione passo-passo con incrudimento
        d_attuale = d0_simulazione
        deformazione_totale = 0
        # Stima del coefficiente di resistenza K dalla legge di Hollomon
        k_resistenza = rm_iniziale / (n_incrudimento**n_incrudimento) * math.exp(n_incrudimento)

        for i, dp in enumerate(passi_da_simulare):
            is_last_pass = (i == len(passi_da_simulare) - 1)
            r_punzone = r_fondo_finale if is_last_pass else r_punzone_intermedio

            # Calcolo deformazione e stato materiale incrudito
            deformazione_passo = math.log(d_attuale / dp)
            deformazione_totale += deformazione_passo
            stress_flusso = k_resistenza * (deformazione_totale ** n_incrudimento)
            rm_attuale = stress_flusso * 1.1 # Stima conservativa del nuovo Rm

            # Calcolo tensione e forze
            tensione_imbutitura = 1.1 * stress_flusso * deformazione_passo
            forza_imb = math.pi * dp * spessore * rm_attuale * 0.7
            area_anello = (math.pi / 4) * (d_attuale ** 2 - dp ** 2)
            forza_pl = area_anello * pressione_target if area_anello > 0 else 0

            # Stampa risultati del passaggio
            print(f"\nPassaggio {i + 1}:")
            print(f"  - UTENSILE: Punzone Ø {dp:.2f} mm, Raggio {r_punzone:.2f} mm")
            print(f"  - MATERIALE: Deformazione Totale: {deformazione_totale:.2f}, Resistenza (Rm) stimata: {rm_attuale:.0f} MPa")
            print(f"  - ANALISI TENSIONE (Rischio Rottura):")
            print(f"    Tensione di Imbutitura: {tensione_imbutitura:.0f} MPa")
            print(f"    Limite di Sicurezza ({soglia_sicurezza*100:.0f}% Rm): {rm_attuale * soglia_sicurezza:.0f} MPa")
            if tensione_imbutitura > rm_attuale * soglia_sicurezza:
                print("    !!! AVVISO CRITICO: Rischio di rottura! La tensione supera il limite di sicurezza.")
            
            print(f"  - ANALISI FORZE (Uso Macchina):")
            print(f"    Forza Imbutitura: {forza_imb / 1000:.2f} kN")
            print(f"    Forza Premilamiera: {forza_pl / 1000:.2f} kN")
            if forza_pl > forza_max_cuscino_N:
                print(f"    ATTENZIONE: Forza premilamiera richiesta supera il massimo del cuscino!")
            if (forza_imb + forza_pl) > forza_max_pressa_N:
                print(f"    ATTENZIONE: Forza totale richiesta supera il massimo della pressa!")

            d_attuale = dp

        print("\n--- Fine Analisi di Processo ---")

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"\nERRORE: Problema con il file 'parametri_imbutitura.csv' o con i dati. Dettagli: {e}")
    except Exception as e:
        print(f"\nSi è verificato un errore inatteso: {e}")
