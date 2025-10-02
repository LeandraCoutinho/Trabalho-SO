from questao_1.simulator.utils import read_json
from questao_1.simulator.core import Simulator
from questao_1.results.tables import display_and_save_results
from questao_1.results.grafics import generate_required_charts
    
CONFIG_FILE = "questao_1/config.json"

def main():
    """Ponto de entrada do programa."""
    
    results = None 
    
    try:
        print(f"Carregando configuração de '{CONFIG_FILE}'...")
        config = read_json(CONFIG_FILE)
        
        simulator = Simulator(config)
        simulator.run_simulation()
        
        results = simulator.get_results()

        if results:
            # Imprime tabelas
            display_and_save_results(results)

            # Gera gráficos
            generate_required_charts(results) 

    except FileNotFoundError:
        print(f"ERRO: Arquivo de configuração '{CONFIG_FILE}' não encontrado.")
    except Exception as e:
        print(f"\nERRO FATAL: Ocorreu um problema durante a simulação: {e}")
        return 

if __name__ == "__main__":
    main()