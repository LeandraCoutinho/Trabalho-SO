from questao_1.simulator.utils import read_json
from questao_1.simulator.core import Simulator
from questao_1.results.tables import display_and_save_results
   
CONFIG_FILE = "config.json"

def main():
    """Ponto de entrada do programa."""
    try:
        print(f"Carregando configuração de '{CONFIG_FILE}'...")
        config = read_json(CONFIG_FILE)
        
        simulator = Simulator(config)
        simulator.run()
        
        results = simulator.get_results()
        display_and_save_results(results)
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo de configuração '{CONFIG_FILE}' não encontrado.")
    except Exception as e:
        print(f"\nERRO FATAL: Ocorreu um problema durante a simulação: {e}")

if __name__ == "__main__":
    main()