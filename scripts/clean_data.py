import csv
import os

# --- CONFIGURACIÓN ---
# Rutas relativas desde la raíz del proyecto
INPUT_FILE = "data/raw/transactions_day_1.csv"
OUTPUT_FILE = "data/processed/cleaned_transactions.csv"

def clean_text(text):
    """
    Limpieza básica: elimina espacios extra y estandariza texto.
    Ejemplo: "  Pan " -> "Pan"
    """
    if not text:
        return None
    return text.strip()

def run_cleaning():
    print("--- Iniciando Limpieza de Datos ---")
    
    # 1. Validar que exista el archivo de entrada
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No se encontró el archivo {INPUT_FILE}")
        return

    processed_count = 0
    
    try:
        # Abrimos el archivo RAW (Lectura) y el PROCESSED (Escritura)
        with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
             open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f_out:
            
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            # Saltamos el encabezado del RAW (TransactionID, Items)
            header = next(reader, None)
            
            # Escribimos un encabezado simple para el archivo limpio
            # Solo nos importa la lista de items
            writer.writerow(["items"]) 

            for row in reader:
                # El formato raw es: [ID, "Item1, Item2, Item3"]
                if len(row) < 2:
                    continue # Saltar filas corruptas
                
                raw_items_string = row[1] # Tomamos la columna de items
                
                # Convertimos "Pan, Leche, Huevos" -> ["Pan", "Leche", "Huevos"]
                items_list = raw_items_string.split(',')
                
                # Limpiamos cada item individualmente
                clean_items = [clean_text(item) for item in items_list]
                
                # Filtramos vacíos (por si hubo ",,")
                clean_items = [i for i in clean_items if i]
                
                # Guardamos en el nuevo CSV como una cadena unida por comas
                # (Airflow o Apriori leerán esto después)
                if clean_items:
                    writer.writerow([",".join(clean_items)])
                    processed_count += 1

        print(f"✅ Limpieza completada.")
        print(f"📄 Datos procesados guardados en: {OUTPUT_FILE}")
        print(f"📊 Total transacciones válidas: {processed_count}")

    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")

if __name__ == "__main__":
    run_cleaning()