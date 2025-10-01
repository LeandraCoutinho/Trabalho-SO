from typing import List, Dict, Any
from .models import Processe
import copy
from .fcfs_sjf import fcfs, sjf 
from .round_robin import round_robin
from .utils import calculate_metrics, format_execution_sequence

class Simulator:
    """
    Controla a execução da simulação.
    """
    def __init__(self, config: Dict[str, Any]):
        self.context_switch_cost = config["metadata"]["context_switch_cost"]
        self.throughput_window_T = config["metadata"]["throughput.window_T"]
        self.algorithms = config["metadata"]["algorithms"]
        self.rr_quantums = config["metadata"]["rr_quantums"]

        self.tempo = 0  # contador global de tempo
        self.fila_prontos: List[Processe] = []
        self.processes: List[Processe] = [
            Processe(**p) for p in config["workload"]["processes"]
        ]

        self.processo_em_execucao: Processe = None
        self.resultados = {
            "execucao": [],
            "metricas": {}
        }

    def run_simulation(self):
        """Executa FCFS, SJF e RR (com seus respectivos quantums)."""
        
       
        for alg in self.algorithms:
            
            current_processes = copy.deepcopy(self.base_processes)

            if alg == "FCFS":
                print("Executando FCFS...")
                completed = fcfs(current_processes)
                self._process_results("FCFS", completed)

            elif alg == "SJF":
                print("Executando SJF (Não-Preemptivo)...")
                completed = sjf(current_processes)
                self._process_results("SJF", completed)

            elif alg == "RR":
                for q in self.rr_quantums:
                    alg_name = f"RR (Q={q})"
                    print(f"Executando {alg_name}...")
                    
                    
                    rr_processes = copy.deepcopy(self.base_processes)
                    
                    completed = round_robin(
                        rr_processes, 
                        quantum=q, 
                        context_switch_cost=self.context_switch_cost
                    )
                    self._process_results(alg_name, completed, quantum=q)
            else:
                print(f"Algoritmo '{alg}' não reconhecido.")
                
        print("\nSimulação concluída!")


    def _process_results(self, alg_name: str, completed_processes: List[Processo], quantum: int = None):
        """Calcula e armazena métricas e a sequência de execução."""
        
        
        self.all_results["execucao"][alg_name] = format_execution_sequence(completed_processes)
        
      
        metrics = calculate_metrics(completed_processes, alg_name)
        if quantum is not None:
            metrics["quantum"] = quantum
            
        self.all_results["metricas"].append(metrics)
        
    def get_results(self) -> Dict[str, Any]:
        """Retorna todos os resultados da simulação."""
        return self.all_results