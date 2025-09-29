import json
from typing import Dict, Any

def read_json(path: str) -> Dict[str, Any]:
    """
    Lê arquivo JSON e retorna como dicionário.
    """
    with open(path, 'r') as file:
        return json.load(file)