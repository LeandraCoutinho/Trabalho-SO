from typing import List, Dict, Any 
from .models import Process
import copy
from .fcfs_sjf import fcfs, sjf 
from .round_robin import round_robin
from .utils import calculate_metrics, calculate_throughput

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
        self.fila_prontos: List[Process] = []
        self.processes: List[Process] = [
            Process(**p) for p in config["workload"]["processes"]
        ]

        self.results: Dict[str, Any] = {"metricas": [], "execucao": {}} 

    def run_simulation(self):
        """Executa a simulação para todos os algoritmos configurados."""
        print("Iniciando simulação...")

        for alg in self.algorithms:
            if alg == "FCFS":
                self._run_fcfs()
            elif alg == "SJF":
                self._run_sjf()
            elif alg == "RR":
                self._run_rr()
            else:
                print(f"Alerta: Algoritmo '{alg}' não reconhecido.")
        
        print("\nSimulação concluída!")

    def _run_fcfs(self):
        print("Executando FCFS...")
        result_tuple = fcfs(self.processes, self.context_switch_cost)
        self._process_results("FCFS", result_tuple)

    def _run_sjf(self):
        print("Executando SJF (Não-Preemptivo)...")
        result_tuple = sjf(self.processes, self.context_switch_cost)
        self._process_results("SJF", result_tuple)

    def _run_rr(self):
        for q in self.rr_quantums:
            alg_name = f"RR (Q={q})"
            print(f"Executando {alg_name}...")
            
            procs_copy = [copy.deepcopy(p) for p in self.processes]

            result_tuple = round_robin(
                procs_copy, 
                quantum=q, 
                context_switch_cost=self.context_switch_cost
            )
            self._process_results(alg_name, result_tuple)

    def _process_results(self, alg_name: str, result_tuple: tuple):
        """Calcula e armazena métricas e a sequência de execução.""" 
        
        
        completed_processes, timeline = result_tuple
        
       
        metrics = calculate_metrics(completed_processes, alg_name, self.throughput_window_T)

        if alg_name.startswith("RR"):
            # Extrai o valor do quantum do nome 
            quantum_val = int(alg_name.split('=')[1].replace(')', ''))
            metrics["quantum"] = quantum_val
        
        # 2. Armazena as métricas em uma lista
        self.results["metricas"].append(metrics)
        
        # 3. Armazena a sequência de execução detalhada 
        self.results["execucao"][alg_name] = completed_processes

    
    def get_results(self):
        """Retorna todos os resultados da simulação."""
        return self.results