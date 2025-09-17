import math
import pandas as pd

# --- Funzione di Analisi Riutilizzabile ---
def analizza_passaggio(nome_passaggio, L, W, h, r_angolo, r_fondo, r_matrice, spessore, rm, a_perc, p_pl, forza_max_pressa_kN, forza_max_cuscino_kN, soglia_allungamento_perc=100):
    """Analizza un singolo passaggio, considerandolo non valido se la deformazione supera la soglia data."""
    print(f"\n--- Analisi Passaggio: {nome_passaggio} (Soglia Sicurezza: {soglia_allungamento_perc}%) ---")
    
    risultati = {'valido': True, 'messaggi': []}
    soglia_allungamento = soglia_allungamento_perc / 100.0

    # 1. Analisi Rischio Rottura Materiale (Formula migliorata)
    strain_critico = math.log(1 + a_perc / 100)
    # La deformazione è una somma di 3 contributi: stiramento angolo, flessione su matrice, flessione su punzone.
    strain_stimato = (h / (15 * r_angolo)) + (spessore / (2 * r_matrice)) + (spessore / (4 * r_fondo))
    
    print(f"Deformazione massima stimata nell'angolo: {strain_stimato:.3f} (Limite materiale: {strain_critico:.3f})")
    
    if strain_stimato > strain_critico:
        risultati['valido'] = False
        risultati['messaggi'].append(f"ALLARME ROTTURA: Deformazione stimata ({strain_stimato:.3f}) supera il limite fisico del materiale.")
    elif strain_stimato > strain_critico * soglia_allungamento:
        risultati['valido'] = False # Invalida il passaggio se la soglia di sicurezza viene superata
        risultati['messaggi'].append(f"PROCESSO CRITICO: Deformazione stimata supera la soglia di sicurezza del {soglia_allungamento_perc}%.")

    # 2. Calcolo Forze (eseguito comunque per completezza)
    area_fondo = L * W - (4 - math.pi) * (r_angolo**2)
    area_pareti = 2 * (L + W) * h
    area_sviluppo_approx = area_fondo + area_pareti
    area_premilamiera = area_sviluppo_approx - area_fondo

    forza_pl_kN = (area_premilamiera * p_pl) / 1000
    print(f"Forza Premilamiera: {forza_pl_kN:.2f} kN")
    if forza_pl_kN > forza_max_cuscino_kN:
        risultati['valido'] = False
        risultati['messaggi'].append(f"ATTENZIONE: Forza premilamiera ({forza_pl_kN:.2f} kN) supera il massimo del cuscino ({forza_max_cuscino_kN} kN).")

    perimetro_imbutitura = 2 * (L - 2 * r_angolo) + 2 * (W - 2 * r_angolo) + 2 * math.pi * r_angolo
    forza_imb_kN = (perimetro_imbutitura * spessore * rm * 0.7) / 1000
    print(f"Forza di Imbutitura: {forza_imb_kN:.2f} kN")

    forza_totale_kN = forza_imb_kN + forza_pl_kN
    print(f"Forza Totale: {forza_totale_kN:.2f} kN")
    if forza_totale_kN > forza_max_pressa_kN:
        risultati['valido'] = False
        risultati['messaggi'].append(f"ATTENZIONE: Forza totale ({forza_totale_kN:.2f} kN) supera il massimo della pressa ({forza_max_pressa_kN} kN).")
    
    if not risultati['messaggi']:
        print("-> Passaggio considerato fattibile.")
    else:
        for msg in risultati['messaggi']:
            print(f"    -> {msg}")

    return risultati

# --- Main Script: Progettista di Processo Rettangolare ---
if __name__ == "__main__":
    try:
        # Costruisce il percorso del CSV relativo allo script
        params = pd.read_csv('progetto_rettangolare.csv').set_index('parametro')['valore'].to_dict()

        print("--- Inizio Progettazione Processo Rettangolare ---")

        # --- NUOVA SEZIONE: CALCOLO GREZZO E INGOMBRI ---
        print("\n=== Stima Dimensioni Lamiera di Partenza ===")

        # Leggi parametri base e nuovi
        L_finale = params['lunghezza_finale']
        W_finale = params['larghezza_finale']
        h_finale = params['altezza_finale']
        r_angolo_finale = params['raggio_angoli_pareti']
        angolo_sformo = params['angolo_sformo_gradi']
        margine_ala = params['margine_ala_premilamiera_mm']

        # 1. Calcolo ingombro massimo con sformo
        delta_sformo = h_finale * math.tan(math.radians(angolo_sformo))
        L_apertura = L_finale + 2 * delta_sformo
        W_apertura = W_finale + 2 * delta_sformo
        print(f"Ingombro massimo pezzo (con sformo a {angolo_sformo}°): {L_apertura:.1f} x {W_apertura:.1f} mm")

        # 2. Stima sviluppo lamiera (area)
        area_fondo = L_finale * W_finale - (4 - math.pi) * (r_angolo_finale**2)
        area_pareti = 2 * (L_finale + W_finale) * h_finale
        area_sviluppo_approx = area_fondo + area_pareti
        print(f"Superficie sviluppata (approssimata): {area_sviluppo_approx:.0f} mm^2")

        # 3. Calcolo dimensioni rettangolo equivalente
        aspect_ratio = L_finale / W_finale
        W_sviluppo = math.sqrt(area_sviluppo_approx / aspect_ratio)
        L_sviluppo = W_sviluppo * aspect_ratio

        # 4. Aggiunta margine premilamiera
        L_grezzo = L_sviluppo + 2 * margine_ala
        W_grezzo = W_sviluppo + 2 * margine_ala
        print(f"Dimensioni stimate del grezzo rettangolare (con margine di {margine_ala} mm per lato):")
        print(f" -> {L_grezzo:.1f} x {W_grezzo:.1f} mm")

        common_params = {
            'spessore': params['spessore_lamiera'], 'rm': params['resistenza_trazione_Rm'],
            'a_perc': params['allungamento_a_rottura_A_perc'], 'p_pl': params['pressione_premilamiera_target_N_mm2'],
            'forza_max_pressa_kN': params['forza_max_pressa_kN'], 'forza_max_cuscino_kN': params['forza_max_cuscino_kN']
        }

        # FASE 1: Tentativo a passaggio singolo con soglia di sicurezza all'84%
        print("\n=== FASE 1: Tentativo di progettazione a passaggio singolo ===")
        analisi_singola = analizza_passaggio(
            nome_passaggio="Passaggio Unico",
            L=params['lunghezza_finale'], W=params['larghezza_finale'], h=params['altezza_finale'],
            r_angolo=params['raggio_angoli_pareti'], 
            r_fondo=params['raggio_raccordo_fondo_finale'], 
            r_matrice=params['raggio_raccordo_matrice_finale'],
            soglia_allungamento_perc=84, # Soglia di sicurezza per la decisione
            **common_params
        )

        if analisi_singola['valido']:
            print("\n--- CONCLUSIONE --- ")
            print("Il processo sembra fattibile in un singolo passaggio con un margine di sicurezza accettabile.")
        else:
            print("\nIl passaggio singolo è risultato troppo critico. Si procede a progettare un processo a due passaggi.")
            
            # FASE 2: PROGETTAZIONE A DUE PASSAGGI
            print("\n=== FASE 2: Progettazione di un processo a due passaggi ===")

            h1 = params['altezza_finale'] * (params['percentuale_altezza_primo_passaggio'] / 100.0)
            r_angolo_1 = params['raggio_angoli_pareti'] * 1.8
            r_fondo_1 = params['raggio_raccordo_fondo_finale'] * 1.5 # Raggio fondo più grande per il primo passo
            delta_h = params['altezza_finale'] - h1
            L1 = params['lunghezza_finale'] + delta_h * 0.7 
            W1 = params['larghezza_finale'] + delta_h * 0.7

            print("\n--- Proposta per Stampo 1° Passaggio ---")
            print(f"  - Altezza (h1): {h1:.2f} mm")
            print(f"  - Raggio Angoli (r_angolo_1): {r_angolo_1:.2f} mm")
            print(f"  - Raggio Fondo (r_fondo_1): {r_fondo_1:.2f} mm")
            print(f"  - Dimensioni stimate (L1xW1): {L1:.2f} x {W1:.2f} mm")

            soglia_validazione_passi = 98

            analisi_passo1 = analizza_passaggio(
                nome_passaggio="1° Passaggio (Imbutitura)",
                L=L1, W=W1, h=h1, r_angolo=r_angolo_1, r_fondo=r_fondo_1,
                r_matrice=params['raggio_raccordo_matrice_primo'],
                soglia_allungamento_perc=soglia_validazione_passi,
                **common_params
            )

            h_passo2 = params['altezza_finale'] - h1
            analisi_passo2 = analizza_passaggio(
                nome_passaggio="2° Passaggio (Ricalibratura)",
                L=params['lunghezza_finale'], W=params['larghezza_finale'], h=h_passo2,
                r_angolo=params['raggio_angoli_pareti'],
                r_fondo=params['raggio_raccordo_fondo_finale'],
                r_matrice=params['raggio_raccordo_matrice_finale'],
                soglia_allungamento_perc=soglia_validazione_passi,
                **common_params
            )

            print("\n--- CONCLUSIONE --- ")
            if analisi_passo1['valido'] and analisi_passo2['valido']:
                print("PROCESSO A DUE PASSAGGI VALIDATO.")
                print("Le dimensioni proposte per lo stampo del 1° passaggio sono considerate idonee.")
            else:
                print("ATTENZIONE: Anche sdoppiando il processo, uno o entrambi i passaggi risultano critici.")
                print("Il componente è complesso. Si consiglia un'analisi specialistica.")

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"\nERRORE: Problema con il file 'progetto_rettangolare.csv' o con i dati. Dettagli: {e}")
    except Exception as e:
        print(f"\nSi è verificato un errore inatteso: {e}")
