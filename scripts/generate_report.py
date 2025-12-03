import csv
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
RULES_FILE = "data/results/association_rules.csv"
ITEMSETS_FILE = "data/results/frequent_itemsets.csv"
REPORT_FILE = "data/results/summary_report.md"

def load_csv(filepath):
    """Carga un CSV en una lista de diccionarios."""
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def main():
    print("--- Generando Reporte Ejecutivo ---")
    
    # Cargar datos
    rules = load_csv(RULES_FILE)
    itemsets = load_csv(ITEMSETS_FILE)
    
    # Preparar métricas
    top_rules = sorted(rules, key=lambda x: float(x['lift']), reverse=True)[:5]
    top_items = sorted(itemsets, key=lambda x: float(x['support']), reverse=True)[:5]
    
    # Escribir reporte en Markdown
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Reporte Diario de Minería de Datos\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 1. Resumen Ejecutivo\n")
        f.write(f"- **Transacciones Analizadas:** (Ver logs de limpieza)\n")
        f.write(f"- **Itemsets Frecuentes Encontrados:** {len(itemsets)}\n")
        f.write(f"- **Reglas de Asociación Descubiertas:** {len(rules)}\n\n")
        
        f.write("## 2. Top 5 Reglas (Mayor Lift)\n")
        f.write("Estas reglas indican las relaciones más fuertes entre productos:\n\n")
        f.write("| Antecedente | Consecuente | Confianza | Lift |\n")
        f.write("|---|---|---|---|\n")
        for r in top_rules:
            f.write(f"| {r['antecedent']} | **{r['consequent']}** | {r['confidence']} | {r['lift']} |\n")
        
        f.write("\n## 3. Top 5 Productos Más Frecuentes\n")
        f.write("| Productos | Soporte (%) |\n")
        f.write("|---|---|\n")
        for i in top_items:
            supp_pct = float(i['support']) * 100
            f.write(f"| {i['itemset']} | {supp_pct:.1f}% |\n")

    print(f"✅ Reporte generado en: {REPORT_FILE}")

if __name__ == "__main__":
    main()