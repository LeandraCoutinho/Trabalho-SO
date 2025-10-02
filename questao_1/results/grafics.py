from typing import Dict, Any
import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'graficos_output')

def _setup_output_dir():
    """Garante que o diretório de saída exista."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_required_charts(results: dict): 
    """Gera e salva os gráficos de barras comparando as métricas exigidas pela questão."""
    _setup_output_dir()
    print("\nGerando gráficos de métricas comparativas...")

    # Prepara os dados para o DataFrame do pandas
    metrics_list = []
    for alg_name, data in results.items():  
        metric_summary = {'Algoritmo': alg_name, **data['metrics']}
        metrics_list.append(metric_summary)

    df = pd.DataFrame(metrics_list)
    if df.empty:
        print("Aviso: Não há dados de métricas para gerar gráficos.")
        return

    # --- Gráfico 1: Tempo Médio de Espera ---
    plt.figure(figsize=(10, 6))
    bars_espera = plt.bar(
        df['Algoritmo'], 
        df['avg_waiting_time'], 
        yerr=df.get('std_waiting_time'),  
        capsize=5, 
        color='skyblue'
    )
    plt.ylabel('Tempo Médio de Espera (ticks)')
    plt.title('Comparativo de Tempo Médio de Espera')
    plt.xticks(rotation=45, ha="right")
    for bar in bars_espera:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom', ha='center')
    plt.tight_layout()
    path_espera = os.path.join(OUTPUT_DIR, "comparativo_tempo_espera.png")
    plt.savefig(path_espera)
    plt.close()
    print(f"Salvo: {path_espera}")

    # --- Gráfico 2: Tempo Médio de Retorno ---
    plt.figure(figsize=(10, 6))
    bars_retorno = plt.bar(
        df['Algoritmo'], 
        df['avg_turnaround_time'], 
        yerr=df.get('std_turnaround_time'),
        capsize=5, 
        color='lightcoral'
    )
    plt.ylabel('Tempo Médio de Retorno (ticks)')
    plt.title('Comparativo de Tempo Médio de Retorno (Turnaround)')
    plt.xticks(rotation=45, ha="right")
    for bar in bars_retorno:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom', ha='center')
    plt.tight_layout()
    path_retorno = os.path.join(OUTPUT_DIR, "comparativo_tempo_retorno.png")
    plt.savefig(path_retorno)
    plt.close()
    print(f"Salvo: {path_retorno}")
    
    # --- Gráfico 3: Vazão (Throughput) ---
    plt.figure(figsize=(10, 6))
    janela = df['throughput_window'].iloc[0]
    bars_vazao = plt.bar(df['Algoritmo'], df['throughput'], color='mediumseagreen')
    plt.ylabel('Processos Concluídos')
    plt.title(f'Comparativo de Vazão (Throughput em T={janela})')
    plt.xticks(rotation=45, ha="right")
    for bar in bars_vazao:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{int(yval)}', va='bottom', ha='center')
    plt.tight_layout()
    path_vazao = os.path.join(OUTPUT_DIR, "comparativo_vazao.png")
    plt.savefig(path_vazao)
    plt.close()
    print(f"Salvo: {path_vazao}")
