import csv
import random
import os

# --- CONFIGURACIÓN ---
# [cite_start]Rutas basadas en la estructura del PDF [cite: 98]
OUTPUT_DIR = "data/raw"
FILENAME = "transactions_day_1.csv"
NUM_TRANSACTIONS = 1000   # Total de clientes simulados
MAX_ITEMS_PER_TX = 8      # Máximo de productos por carrito

# [cite_start]20 Productos (Universo del Itemset: 5-20 items permitidos [cite: 50])
ITEMS = [
    "Leche", "Pan", "Huevos", "Mantequilla", "Queso",
    "Manzanas", "Platanos", "Cerveza", "Panales", "Refresco",
    "Papas fritas", "Cebolla", "Pasta", "Salsa de Tomate",
    "Cafe", "Azucar", "Detergente", "Papel Higienico",
    "Yogur", "Chocolate"
]

# Reglas Sesgadas (Bias) para asegurar que Apriori encuentre patrones interesantes
# Formato: (Si compra A, Probabilidad de que compre B)
RULES_TO_INJECT = [
    ("Pasta", "Salsa de Tomate", 0.85),  # Regla muy fuerte
    ("Cafe", "Azucar", 0.70),            # Regla media
    ("Panales", "Cerveza", 0.60),        # El clásico ejemplo
    ("Pan", "Mantequilla", 0.50),
    ("Cerveza", "Papas fritas", 0.65),
    ("Leche", "Chocolate", 0.40)
]

def generate_transaction(tx_id):
    """Genera una transacción simulada con inyección de patrones."""
    # 1. Selección aleatoria base
    num_items = random.randint(1, MAX_ITEMS_PER_TX)
    basket = set(random.sample(ITEMS, num_items))

    # 2. Inyección de patrones
    # Si el item "trigger" ya está en la canasta, intentamos agregar su par
    for main_item, co_item, probability in RULES_TO_INJECT:
        if main_item in basket:
            if random.random() < probability:
                basket.add(co_item)
    
    # [cite_start]Formato string requerido por el PDF: "Item1, Item2, Item3" [cite: 20]
    items_str = ", ".join(basket)
    
    # Estructura [ID, "Items"]
    return [tx_id, f'"{items_str}"']

def main():
    # Crear carpeta si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, FILENAME)

    print(f"--- Generando Datos Simulados ---")
    print(f"Transacciones: {NUM_TRANSACTIONS}")
    print(f"Universo de Items: {len(ITEMS)}")
    
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Header
            writer.writerow(["TransactionID", "Items"])
            
            # Filas
            for i in range(1, NUM_TRANSACTIONS + 1):
                writer.writerow(generate_transaction(i))

        print(f"✅ Éxito: Archivo guardado en {file_path}")
        
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")

if __name__ == "__main__":
    main()