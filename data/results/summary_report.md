# Reporte Diario de Minería de Datos
**Fecha:** 2025-12-02 16:51:28

## 1. Resumen Ejecutivo
- **Transacciones Analizadas:** (Ver logs de limpieza)
- **Itemsets Frecuentes Encontrados:** 156
- **Reglas de Asociación Descubiertas:** 239

## 2. Top 5 Reglas (Mayor Lift)
Estas reglas indican las relaciones más fuertes entre productos:

| Antecedente | Consecuente | Confianza | Lift |
|---|---|---|---|
| Papas fritas", Azucar | **Cafe, Cerveza** | 0.4 | 4.4944 |
| Cafe, Cerveza | **Papas fritas", Azucar** | 0.6292 | 4.4944 |
| Pasta, Papas fritas" | **Salsa de Tomate, Cerveza** | 0.6196 | 4.4573 |
| Salsa de Tomate, Cerveza | **Pasta, Papas fritas"** | 0.4101 | 4.4573 |
| Salsa de Tomate, Papas fritas" | **Pasta, Cerveza** | 0.3677 | 4.4306 |

## 3. Top 5 Productos Más Frecuentes
| Productos | Soporte (%) |
|---|---|
| Papas fritas" | 35.1% |
| Cerveza | 28.7% |
| Salsa de Tomate | 28.5% |
| Azucar | 27.1% |
| Papas fritas", Cerveza | 23.5% |
