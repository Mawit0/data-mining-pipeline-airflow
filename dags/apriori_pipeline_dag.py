from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DEL DAG ---
default_args = {
    'owner': 'mauricio_data_lab',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definimos el DAG
with DAG(
    'market_basket_analysis_pipeline',
    default_args=default_args,
    description='Pipeline completo de mineria de datos: Ingesta -> Limpieza -> Apriori -> Reporte',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['data_mining', 'apriori'],
) as dag:

    # --- DEFINICIÓN DE TAREAS ---
    
    # Tarea 1: Simulación de Ingesta
    t1_generate_data = BashOperator(
        task_id='ingest_simulate_data',
        bash_command='cd /opt/airflow && python scripts/generate_data.py',
        doc_md="Simula la llegada diaria de archivos CSV de transacciones."
    )

    # Tarea 2: Limpieza y Preprocesamiento
    t2_clean_data = BashOperator(
        task_id='clean_preprocessing',
        bash_command='cd /opt/airflow && python scripts/clean_data.py',
        doc_md="Limpia los datos crudos eliminando IDs y formateando listas."
    )

    # Tarea 3: Minería de Reglas (Apriori)
    t3_run_apriori = BashOperator(
        task_id='run_apriori_algorithm',
        bash_command='cd /opt/airflow && python scripts/apriori.py',
        doc_md="Ejecuta el algoritmo Apriori personalizado."
    )

    # Tarea 4: Generación de Reporte
    t4_generate_report = BashOperator(
        task_id='generate_final_report',
        bash_command='cd /opt/airflow && python scripts/generate_report.py',
        doc_md="Genera un reporte resumen con las reglas encontradas."
    )

    # --- ORQUESTACIÓN ---
    t1_generate_data >> t2_clean_data >> t3_run_apriori >> t4_generate_report