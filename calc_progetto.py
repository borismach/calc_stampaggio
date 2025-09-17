import math
import pandas as pd

# --- Funzioni di Calcolo e Simulazione (riutilizzate dall'Analista) ---
def calcola_diametro_disco_iniziale(d_finale, h_finale, r_fondo):
    """Calcola il diametro teorico netto del disco di partenza."""
    if r_fondo == 0:
        return math.sqrt(d_finale ** 2 + 4 * d_finale * h_finale)
    return math.sqrt((d_finale - 2 * r_fondo) ** 2 + 4 * d_finale * (h_finale - r_fondo) + 
                     2 * math.pi * r_fondo * (d_finale - 0.7 * r_fondo))

def calcola_sequenza_passaggi(d0, d_finale, ldr1, ldrn):
    """Calcola la sequenza di diametri dei punzoni basandosi su LDR fissi."""
    diametri = []
    d_attuale = d0
    if d0 <= d_finale: return []

    # 1° Passaggio
    d_attuale /= ldr1
    diametri.append(d_attuale)

    # Passaggi successivi
    while d_attuale > d_finale:
        prossimo_d = d_attuale / ldrn
        if prossimo_d < d_finale:
            if abs(d_attuale - d_finale) > 1e-6:
                diametri.append(d_finale)
            break
        d_attuale = prossimo_d
        diametri.append(d_attuale)
        if len(diametri) > 20: return None # Limite di sicurezza
    return diametri

# --- Main Script: Calcolatrice di Processo ---
if __name__ == "__main__":
    try:
        params = pd.read_csv('progetto_imbutitura.csv').set_index('parametro')['valore'].to_dict()

        print("--- Inizio Progettazione Nuovo Processo di Imbutitura ---")

        # Caricamento parametri dal CSV di progetto
        d_finale = params['diametro_finale_cilindro']
        h_finale = params['altezza_finale_cilindro']
        r_fondo_finale = params['raggio_raccordo_fondo']
        r_punzone_intermedio = params['raggio_punzone_intermedio_mm']
        spessore = params['spessore_lamiera']
        rm_iniziale = params['resistenza_trazione_Rm']
        rp02_iniziale = params['limite_snervamento_Rp02']
        n_incrudimento = params['coefficiente_incrudimento_n']
        ldr1 = params['ldr_primo_passaggio_progetto']
        ldrn = params['ldr_passaggi_successivi_progetto']
        pressione_target = params['pressione_premilamiera_target_N_mm2']
        forza_max_pressa_N = params['forza_max_pressa'] * 1000
        forza_max_cuscino_N = params['forza_max_cuscino_kN'] * 1000
        soglia_sicurezza = 0.90 # Usiamo una soglia conservativa per i nuovi progetti

        # 1. Calcolo del diametro del disco di partenza
        d0 = calcola_diametro_disco_iniziale(d_finale, h_finale, r_fondo_finale)
        print(f"\nDiametro teorico del disco (D0) calcolato: {d0:.2f} mm (non include flangia per premilamiera)")

        # 2. Generazione della sequenza di passaggi basata su LDR standard
        passi_proposti = calcola_sequenza_passaggi(d0, d_finale, ldr1, ldrn)
        if not passi_proposti:
            raise ValueError("Impossibile generare una sequenza di passaggi con i dati LDR forniti.")

        print(f"\nProposta di un processo a {len(passi_proposti)} passaggi (LDR1={ldr1}, LDRn={ldrn})...")
        print("--- Inizio Validazione e Analisi di Processo ---")

        # 3. Esecuzione della simulazione sul processo proposto
        d_attuale = d0
        deformazione_totale = 0
        k_resistenza = rm_iniziale / (n_incrudimento**n_incrudimento) * math.exp(n_incrudimento)
        processo_valido = True

        for i, dp in enumerate(passi_proposti):
            is_last_pass = (i == len(passi_proposti) - 1)
            r_punzone = r_fondo_finale if is_last_pass else r_punzone_intermedio

            # Calcolo deformazione e stato materiale incrudito
            deformazione_passo = math.log(d_attuale / dp)
            deformazione_totale += deformazione_passo
            stress_flusso = k_resistenza * (deformazione_totale ** n_incrudimento)
            rm_attuale = stress_flusso * 1.1

            # Calcolo tensione e forze
            tensione_imbutitura = 1.1 * stress_flusso * deformazione_passo
            forza_imb = math.pi * dp * spessore * rm_attuale * 0.7
            area_anello = (math.pi / 4) * (d_attuale ** 2 - dp ** 2)
            forza_pl = area_anello * pressione_target if area_anello > 0 else 0

            # Stampa risultati del passaggio
            print(f"\nPassaggio {i + 1}:")
            print(f"  - UTENSILE PROPOSTO: Punzone Ø {dp:.2f} mm, Raggio {r_punzone:.2f} mm")
            print(f"  - MATERIALE: Deformazione Totale: {deformazione_totale:.2f}, Resistenza (Rm) stimata: {rm_attuale:.0f} MPa")
            print(f"  - ANALISI TENSIONE (Rischio Rottura):")
            print(f"    Tensione di Imbutitura: {tensione_imbutitura:.0f} MPa")
            print(f"    Limite di Sicurezza ({soglia_sicurezza*100:.0f}% Rm): {rm_attuale * soglia_sicurezza:.0f} MPa")
            if tensione_imbutitura > rm_attuale * soglia_sicurezza:
                print("    !!! AVVISO CRITICO: Rischio di rottura! La tensione supera il limite di sicurezza.")
                processo_valido = False
            
            print(f"  - ANALISI FORZE (Uso Macchina):")
            print(f"    Forza Imbutitura: {forza_imb / 1000:.2f} kN")
            print(f"    Forza Premilamiera: {forza_pl / 1000:.2f} kN")
            if forza_pl > forza_max_cuscino_N:
                print(f"    ATTENZIONE: Forza premilamiera richiesta supera il massimo del cuscino!")
            if (forza_imb + forza_pl) > forza_max_pressa_N:
                print(f"    ATTENZIONE: Forza totale richiesta supera il massimo della pressa!")

            d_attuale = dp

        print("\n--- Fine Progettazione ---")
        if processo_valido:
            print("Il processo proposto è stato validato e risulta sicuro secondo il modello di simulazione.")
        else:
            print("ATTENZIONE: Il processo proposto presenta rischi di rottura. Considerare LDR più bassi o più passaggi.")

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"\nERRORE: Problema con il file 'progetto_imbutitura.csv' o con i dati. Dettagli: {e}")
    except Exception as e:
        print(f"\nSi è verificato un errore inatteso: {e}")
