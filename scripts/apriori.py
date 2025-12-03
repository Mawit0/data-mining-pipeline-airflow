import csv
import itertools
import os

# --- CONFIGURACIÓN ---
INPUT_FILE = "data/processed/cleaned_transactions.csv"
OUTPUT_ITEMSETS = "data/results/frequent_itemsets.csv"
OUTPUT_RULES = "data/results/association_rules.csv"

# Parámetros mínimos (Ajustables según los resultados)
MIN_SUPPORT = 0.05      # El ítem debe aparecer en el 5% de las transacciones
MIN_CONFIDENCE = 0.30   # La regla debe cumplirse el 30% de las veces
MIN_LIFT = 1.1          # Lift > 1 indica correlación positiva

def load_transactions():
    """Carga las transacciones limpias en una lista de sets."""
    transactions = []
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No existe {INPUT_FILE}")
        return []
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None) # Saltar header
        for row in reader:
            if row:
                # row[0] es "Pan,Leche,Huevos". Lo convertimos a set python
                transactions.append(set(row[0].split(',')))
    return transactions

def get_support(itemset, transactions):
    """Calcula el soporte: % de transacciones que contienen el itemset."""
    count = 0
    for t in transactions:
        if itemset.issubset(t):
            count += 1
    return count / len(transactions)

def get_frequent_itemsets(transactions, min_support):
    """
    Núcleo de Apriori: Encuentra todos los itemsets frecuentes.
    """
    print("🔍 Buscando itemsets frecuentes...")
    frequent_itemsets = {} # Diccionario {frozenset: support}
    
    # Paso 1: Itemsets de tamaño 1 (C1)
    # Contamos ocurrencias individuales
    item_counts = {}
    for t in transactions:
        for item in t:
            item_s = frozenset([item])
            item_counts[item_s] = item_counts.get(item_s, 0) + 1
            
    n_trans = len(transactions)
    
    # Filtramos por soporte mínimo (L1)
    current_L = {}
    for itemset, count in item_counts.items():
        support = count / n_trans
        if support >= min_support:
            current_L[itemset] = support
    
    frequent_itemsets.update(current_L)
    print(f"   -> Encontrados {len(current_L)} items individuales frecuentes.")

    # Paso 2: Iterar para k=2, k=3, etc.
    k = 2
    while current_L:
        # Generar candidatos (Ck) uniendo itemsets de L(k-1)
        prev_itemsets = list(current_L.keys())
        candidates = set()
        
        for i in range(len(prev_itemsets)):
            for j in range(i + 1, len(prev_itemsets)):
                # Unimos dos sets
                union = prev_itemsets[i] | prev_itemsets[j]
                if len(union) == k:
                    candidates.add(union)
        
        # Calcular soporte para candidatos y filtrar
        next_L = {}
        for cand in candidates:
            support = get_support(cand, transactions)
            if support >= min_support:
                next_L[cand] = support
        
        if not next_L:
            break
            
        print(f"   -> Encontrados {len(next_L)} itemsets frecuentes de tamaño {k}.")
        frequent_itemsets.update(next_L)
        current_L = next_L
        k += 1
        
    return frequent_itemsets

def generate_association_rules(frequent_itemsets, transactions, min_confidence, min_lift):
    """
    Genera reglas A -> B basándose en los itemsets frecuentes.
    Calcula Confianza y Lift.
    """
    print("🧠 Generando reglas de asociación...")
    rules = []
    
    for itemset, support_AB in frequent_itemsets.items():
        # Solo generamos reglas si el itemset tiene más de 1 elemento
        if len(itemset) > 1:
            # Generamos todas las combinaciones posibles de antecedentes
            # Ej: Si itemset es {A, B}, antecedente puede ser {A} o {B}
            for i in range(1, len(itemset)):
                for antecedent in itertools.combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    
                    support_A = frequent_itemsets.get(antecedent)
                    support_B = get_support(consequent, transactions) # Costoso pero necesario para Lift
                    
                    if support_A:
                        confidence = support_AB / support_A
                        lift = confidence / support_B
                        
                        if confidence >= min_confidence and lift >= min_lift:
                            rules.append({
                                'antecedent': list(antecedent),
                                'consequent': list(consequent),
                                'support': round(support_AB, 4),
                                'confidence': round(confidence, 4),
                                'lift': round(lift, 4)
                            })
    return rules

def save_results(frequent_itemsets, rules):
    """Guarda los resultados en CSVs según pide el PDF."""
    os.makedirs(os.path.dirname(OUTPUT_ITEMSETS), exist_ok=True)
    
    # 1. Guardar Itemsets
    with open(OUTPUT_ITEMSETS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['itemset', 'support'])
        # Ordenamos por soporte descendente
        sorted_items = sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True)
        for itemset, support in sorted_items:
            writer.writerow([", ".join(list(itemset)), round(support, 4)])
            
    # 2. Guardar Reglas
    with open(OUTPUT_RULES, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['antecedent', 'consequent', 'support', 'confidence', 'lift'])
        # Ordenamos por lift descendente
        sorted_rules = sorted(rules, key=lambda x: x['lift'], reverse=True)
        for r in sorted_rules:
            writer.writerow([
                ", ".join(r['antecedent']),
                ", ".join(r['consequent']),
                r['support'],
                r['confidence'],
                r['lift']
            ])
            
    print(f"✅ Resultados guardados en data/results/")

def main():
    transactions = load_transactions()
    if not transactions:
        return

    print(f"--- Iniciando Algoritmo Apriori ---")
    print(f"Transacciones: {len(transactions)}")
    
    # 1. Encontrar frecuentes
    freq_itemsets = get_frequent_itemsets(transactions, MIN_SUPPORT)
    
    # 2. Generar reglas
    rules = generate_association_rules(freq_itemsets, transactions, MIN_CONFIDENCE, MIN_LIFT)
    
    # 3. Guardar
    save_results(freq_itemsets, rules)
    print(f"📊 Total Reglas encontradas: {len(rules)}")

if __name__ == "__main__":
    main()