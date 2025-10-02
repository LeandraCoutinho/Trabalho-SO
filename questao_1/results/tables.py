import os
import pandas as pd
from dataclasses import asdict

OUTPUT_TABLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'output_tables')

def save_table(df: pd.DataFrame, filename: str):
    """Salva a tabela no formato CSV na pasta de resultados."""
    if not os.path.exists(OUTPUT_TABLES_DIR):
        os.makedirs(OUTPUT_TABLES_DIR)
    path = os.path.join(OUTPUT_TABLES_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Tabela de resultados salva em: {path}")

def display_and_save_results(results: dict):
    """Exibe a sequência de execução e a tabela de métricas, e salva os dados."""
    
    print("\n" + "=" * 60)
    print("                RESULTADOS DA SIMULAÇÃO                ")
    print("                (RR vs FCFS vs SJF)                    ")
    print("=" * 60)
    
    
    print("\n## 1. Tabela de Métricas (Média de Espera, Retorno e Vazão)")
    
    metrics_list = []
    for alg_name, data in results.items():
        metric_summary = {'Algoritmo': alg_name, **data['metrics']}
        metrics_list.append(metric_summary)

    df_metrics = pd.DataFrame(metrics_list)
    
    display_columns = {
        'Algoritmo': 'Algoritmo',
        'avg_waiting_time': 'Tempo Médio de Espera',
        'std_waiting_time': 'Desvio Padrão (Espera)',
        'avg_turnaround_time': 'Tempo Médio de Retorno',
        'std_turnaround_time': 'Desvio Padrão (Retorno)',
        'throughput': 'Vazão (Throughput)'
    }

    # Filtra apenas as colunas que realmente existem para evitar erros
    existing_cols = [col for col in display_columns.keys() if col in df_metrics.columns]
    df_metrics_display = df_metrics[existing_cols].rename(columns=display_columns)
    
    print(df_metrics_display.to_string(index=False, float_format="%.2f"))
    save_table(df_metrics_display, "metricas_comparativas.csv")

    print("\n" + "-" * 60)
    print("## 2. Detalhamento da Sequência de Execução (Tempos Finais)")
    
    for alg_name, data in results.items():
        print(f"\n--- {alg_name} ---")
        
        # Converte a lista de objetos Process em uma lista de dicionários para o pandas
        procs_as_dicts = [asdict(p) for p in data['completed_processes']]
        df_procs = pd.DataFrame(procs_as_dicts)

        # Mapeia os nomes das colunas de inglês para português
        column_mapping = {
            'pid': 'PID', 'arrival_time': 'Chegada', 'burst_time': 'Duração (Burst)',
            'start_time': 'Início', 'finish_time': 'Fim', 
            'waiting_time': 'Tempo de Espera', 'turnaround_time': 'Tempo de Retorno'
        }
        existing_proc_cols = [col for col in column_mapping.keys() if col in df_procs.columns]
        df_procs_display = df_procs[existing_proc_cols].rename(columns=column_mapping)
        
        print(df_procs_display.to_string(index=False))
        
        # Salva a tabela de detalhamento em um arquivo CSV
        safe_alg_name = alg_name.replace(' ', '_').replace('=', '').replace('(', '').replace(')', '')
        save_table(df_procs_display, f"detalhes_{safe_alg_name}.csv")