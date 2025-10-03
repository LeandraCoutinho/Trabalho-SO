from .simulator.utils import read_json
from .simulator.core import Simulator
from .results.tables import display_and_save_results
from .results.grafics import generate_required_charts

CONFIG_FILE = "questao_1/config.json"

def run():
    print(f"Carregando configuração de '{CONFIG_FILE}'...")
    config = read_json(CONFIG_FILE)
    simulator = Simulator(config)
    simulator.run_simulation()

    results = simulator.get_results()
    if results:
        display_and_save_results(results)
        generate_required_charts(results)