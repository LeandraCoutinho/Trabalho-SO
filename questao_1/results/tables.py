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
    
    df_metrics = pd.DataFrame(results["metricas"])
    
 
    df_metrics_display = df_metrics[[
        'algoritmo', 
        'quantum', 
        'tempo_medio_espera', 
        'tempo_medio_retorno', 
        'vazao'
    ]].fillna({'quantum': '-'})

    
    format_mapping = {
        col: '{:.2f}'.format for col in df_metrics_display.select_dtypes(include=['float64']).columns
    }
    
    print(df_metrics_display.to_string(index=False, formatters=format_mapping))
    save_table(df_metrics_display, "metricas_comparativas.csv")

    print("\n" + "-" * 60)
    print("## 2. Detalhamento da Sequência de Execução (Tempos Finais)")
    
    for alg_name, exec_seq in results["execucao"].items():
        print(f"\n--- Algoritmo: {alg_name} ---")
        df_exec = pd.DataFrame(exec_seq)
        
        df_exec = df_exec[['pid', 'chegada', 'burst', 'inicio', 'fim', 'espera', 'retorno']]
        
        print(df_exec.to_string(index=False))
        save_table(df_exec, f"execucao_{alg_name.replace(' ', '_').replace('=', '')}.csv")
    
    print("=" * 60)
    print("Simulação concluída. Pronto para a apresentação/demonstração.")