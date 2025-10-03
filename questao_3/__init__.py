import json
from collections import deque

def simulate_room(data):
    animals = sorted(
        data["workload"]["animals"],
        key=lambda x: (x["arrival_time"], x["id"])
    )
    
    timeline = []
    current_state = "EMPTY"
    room_species = None
    inside = []  # animais na sala (id, species, exit_time)
    waiting = deque()
    time = 0
    
    # determinar o tempo máximo da simulação
    max_time = max(a["arrival_time"] + a["rest_duration"] for a in animals) + 1
    
    while time <= max_time or inside:
        # chegada de novos animais
        for a in [a for a in animals if a["arrival_time"] == time]:
            if current_state == "EMPTY":
                current_state = "DOGS" if a["species"] == "DOG" else "CATS"
                room_species = a["species"]
                inside.append((a["id"], a["species"], time + a["rest_duration"]))
                timeline.append({"time": time, "state": current_state})
            elif a["species"] == room_species:
                inside.append((a["id"], a["species"], time + a["rest_duration"]))
            else:
                waiting.append(a)
        
        # saída de animais cujo tempo acabou
        before = len(inside)
        inside = [(i, s, t_exit) for (i, s, t_exit) in inside if t_exit > time]
        after = len(inside)
        
        # sala pode ter mudado
        if before > 0 and after == 0:
            current_state = "EMPTY"
            room_species = None
            timeline.append({"time": time, "state": "EMPTY"})
            
            # tentar colocar alguém da fila de espera
            new_waiting = deque()
            while waiting:
                w = waiting.popleft()
                if current_state == "EMPTY":
                    current_state = "DOGS" if w["species"] == "DOG" else "CATS"
                    room_species = w["species"]
                    inside.append((w["id"], w["species"], time + w["rest_duration"]))
                    timeline.append({"time": time, "state": current_state})
                elif w["species"] == room_species:
                    inside.append((w["id"], w["species"], time + w["rest_duration"]))
                else:
                    new_waiting.append(w)
            waiting = new_waiting
        
        time += 1
    
    return {"timeline": timeline}


def run():
    """Executa a simulação da Questão 3."""
    data = {
        "spec_version": "1.0",
        "challenge_id": "vet.room.protocol.demo",
        "metadata": {
            "room_count": 1,
            "allowed_states": ["EMPTY", "DOGS", "CATS"],
            "queue_policy": "FIFO",
            "sign_change_latency": 0,
            "tie_breaker": ["arrival_time", "id"]
        },
        "room": {
            "initial_sign_state": "EMPTY"
        },
        "workload": {
            "time_unit": "ticks",
            "animals": [
                {"id": "D01", "species": "DOG", "arrival_time": 0, "rest_duration": 5},
                {"id": "C01", "species": "CAT", "arrival_time": 1, "rest_duration": 4},
                {"id": "D02", "species": "DOG", "arrival_time": 2, "rest_duration": 3},
                {"id": "C02", "species": "CAT", "arrival_time": 3, "rest_duration": 2},
                {"id": "D03", "species": "DOG", "arrival_time": 4, "rest_duration": 3}
            ]
        }
    }

    result = simulate_room(data)
    print("\n=== Questão 3 ===")
    print(json.dumps(result, indent=2))