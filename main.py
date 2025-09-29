from questao_1.simulator.utils import read_json
from questao_1.simulator.core import Simulator

if __name__ == "__main__":
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

    simulador = Simulator(json_exemplo)
    print(simulador)