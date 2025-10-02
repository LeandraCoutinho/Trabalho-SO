import json
from typing import Dict, Any
from typing import List, Dict, Any
from .models import Process
import statistics

def read_json(path: str) -> Dict[str, Any]:
    """
    Lê arquivo JSON e retorna como dicionário.
    """
    with open(path, 'r') as file:
        return json.load(file)
    
def calculate_throughput(processes: List[Process], time_window: int) -> int:
    """
    Calcula quantos processos foram concluídos dentro da janela de tempo especificada.
    """
    return len([
        p for p in processes 
        if p.finish_time is not None and p.finish_time <= time_window
    ])

def calculate_metrics(
    processes: List[Process], 
    alg_name: str, 
    throughput_window: int
) -> Dict[str, Any]:
    """
    Calcula as métricas de desempenho a partir de uma lista de processos finalizados.
    """
    if not processes:
        return {
            "algoritmo": alg_name, "avg_turnaround_time": 0, "avg_waiting_time": 0,
            "avg_response_time": 0, "cpu_utilization": 0, "throughput": 0,
            "std_turnaround_time": 0, "std_waiting_time": 0, "std_response_time": 0
        }

    # Coleta os dados diretamente, confiando nos atributos e propriedades
    turnaround_times = [p.turnaround_time_process for p in processes]
    waiting_times = [p.waiting_time for p in processes]
    response_times = [p.response_time for p in processes]

    total_simulation_time = max(p.finish_time for p in processes)
    total_busy_time = sum(p.burst_time for p in processes)

    metrics = {
        "algoritmo": alg_name,
        "avg_turnaround_time": statistics.mean(turnaround_times),
        "avg_waiting_time": statistics.mean(waiting_times),
        "avg_response_time": statistics.mean(response_times),
        "cpu_utilization": (total_busy_time / total_simulation_time) * 100 if total_simulation_time > 0 else 0,
        "throughput": calculate_throughput(processes, throughput_window),
        "throughput_window": throughput_window
    }
    
    # Adiciona desvio padrão
    if len(processes) > 1:
        metrics["std_turnaround_time"] = statistics.stdev(turnaround_times)
        metrics["std_waiting_time"] = statistics.stdev(waiting_times)
        metrics["std_response_time"] = statistics.stdev(response_times)
    else:
        metrics["std_turnaround_time"] = 0
        metrics["std_waiting_time"] = 0
        metrics["std_response_time"] = 0

    return metrics