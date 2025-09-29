from typing import List, Dict, Any
from .models import Processe

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

    def __repr__(self):
        return (f"Simulador(tempo={self.tempo}, "
                f"processos={[p.pid for p in self.processes]}, "
                f"fila={[p.pid for p in self.fila_prontos]})")