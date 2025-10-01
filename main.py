import os
import pandas as pd 
from questao_1.simulator.utils import read_json
from questao_1.simulator.core import Simulator

OUTPUT_TABLES_DIR = "resultados/tabelas"

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
    
def main():
    """Ponto de entrada do programa."""
    json_exemplo = {
        "spec_version": "1.0",
        "challenge_id": "rr_fcfs_sjf_demo",
        "metadata": {
            "context_switch_cost": 1,
            "throughput.window_T": 100,
            "algorithms": ["FCFS", "SJF", "RR"],
            "rr_quantums": [1, 2, 4, 8, 16]
        },
        "workload": {
            "time_unit": "ticks",
            "processes": [
                {"pid": "P01", "arrival_time": 0, "burst_time": 5},
                {"pid": "P02", "arrival_time": 1, "burst_time": 17},
                {"pid": "P03", "arrival_time": 2, "burst_time": 3},
                {"pid": "P04", "arrival_time": 4, "burst_time": 22},
                {"pid": "P05", "arrival_time": 6, "burst_time": 7}
            ]
        }
    }
try:
       
        simulator = Simulator(json_exemplo)
        simulator.run_simulation()
        
       
        results = simulator.get_results()
        display_and_save_results(results)
        
    except Exception as e:
        print(f"\nFATAL: Ocorreu um erro durante a execução da simulação: {e}")

if __name__ == "__main__":
    main()