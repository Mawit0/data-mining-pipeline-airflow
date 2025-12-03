# Data Mining Pipeline: Market Basket Analysis with Airflow & Apriori

[![Airflow](https://img.shields.io/badge/Apache%20Airflow-Automation-blue)]()
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)]()
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()

## 📘 Overview

This repository contains a fully automated **Data Mining Pipeline** designed for Market Basket Analysis using a custom implementation of the **Apriori algorithm** (no external ML libraries). All ETL and mining tasks are orchestrated through **Apache Airflow** and deployed in a **Docker-based environment**.

The system generates synthetic retail transactions, cleans and processes the data, identifies frequent itemsets and association rules, and produces an executive report containing key business metrics such as **Support**, **Confidence**, and **Lift**.

## 🏗️ Architecture

```mermaid
graph TD
    classDef data fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef process fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    subgraph "1. Ingestion (Extract)"
        A[Data Generator] -->|Python Script| B(transactions_day_1.csv);
        class B data;
    end

    B --> T1[Task: Ingest & Simulate];
    class T1 process;

    subgraph "2. Transformation (Clean)"
        T1 --> T2[Task: Clean & Preprocessing];
        class T2 process;
        T2 -->|ID Removal & Normalization| C(cleaned_transactions.csv);
        class C data;
    end

    subgraph "3. Mining (Apriori Algorithm)"
        C --> T3[Task: Run Apriori];
        class T3 process;
        T3 -->|Mathematical Processing| D(frequent_itemsets.csv);
        T3 -->|Rules + Metrics| E(association_rules.csv);
        class D,E data;
    end

    subgraph "4. Reporting (Load/Viz)"
        D & E --> T4[Task: Generate Report];
        class T4 process;
        T4 --> F(summary_report.md);
        class F report;
    end
```

## 📂 Project Structure

```
project/
├── dags/                   
│   └── apriori_pipeline.py
├── data/                           
│   ├── raw/                
│   ├── processed/          
│   └── results/            
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── apriori.py
│   └── generate_report.py
├── docker-compose.yaml
└── README.md
```

## 🛒 Dataset Simulation

The dataset is generated synthetically to emulate real-world retail transactions:
- 20 grocery products
- 1000 daily transactions
- Probabilistic item correlations
- Ensures the Apriori algorithm identifies meaningful rules

## ⏱️ Pipeline (Airflow DAG)

The Airflow DAG `market_basket_analysis_pipeline` runs daily and contains four sequential tasks:
1. **ingest_simulate_data**
2. **clean_preprocessing**
3. **run_apriori_algorithm**
4. **generate_final_report**

## 🧮 Apriori Algorithm

Pure Python implementation located in `/scripts/apriori.py`.  
Includes Support, Confidence, Lift, candidate generation, and Apriori pruning.

## 🚀 How to Run

Clone and start the environment:

```bash
git clone https://github.com/Mawit0/data-mining-pipeline-airflow.git
cd data-mining-pipeline-airflow
docker compose up airflow-init
docker compose up -d
```

Airflow URL: http://localhost:8080  
User: airflow  
Password: airflow  

## 📊 Outputs

Generated under `data/results/`:
| File | Description |
|------|-------------|
| frequent_itemsets.csv | Frequent itemsets |
| association_rules.csv | Association rules with metrics |
| summary_report.md | Executive insights |

## 🚧 Limitations & Future Work

- In-memory Apriori (limited scalability)
- Local storage only

Future improvements:
- Spark FP-Growth
- Cloud storage integration
- Real-time dashboard
