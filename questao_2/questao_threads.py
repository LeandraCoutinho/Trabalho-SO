import threading  # usado para criar threads, cada programador roda numa thread separada.
import time       # para pausas (sleep) e marcar horários nas mensagens
import random     # para gerar tempos aleatórios de "pensar" e "compilar", simulando comportamento humano.

NUM_PROGRAMMERS = 5

# semáforo para o banco de dependências (máx 2 acessos simultâneos)
db_sem = threading.Semaphore(2)

# semáforo para o compilador (exclusivo)
compiler_sem = threading.Semaphore(1)

# para imprimir estados de forma atômica e armazenar estados
print_lock = threading.Lock()
states_lock = threading.Lock()
states = ["PENSANDO"] * NUM_PROGRAMMERS  
# estados: PENSANDO, ESPERANDO_DB, ESPERANDO_COMPILADOR, COMPILANDO

# essa função imprime uma linha com os estados de todos os programadores e o horário.
def print_states():
    with print_lock:
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}] "
        for i, s in enumerate(states):
            line += f"P{i+1}:{s}   |   "
        print(line)

# repetem para sempre: pensar → esperar DB → esperar compilador → compilar → liberar → pensar de novo
def programmer(i: int):
    global states
    rnd = random.Random(i)  # semente por thread para reproducibilidade leve
    while True:
        # pensa (descansa)
        with states_lock:
            states[i] = "PENSANDO"
        print_states()
        time.sleep(rnd.uniform(1.0, 3.0))  # tempo de "pensar"

        # quer compilar: primeiro tenta obter vaga no DB
        with states_lock:
            states[i] = "ESPERANDO_DB"
        print_states()

        db_acquired = False
        # Bloqueia até conseguir vaga no DB (máx 2)
        db_sem.acquire()
        db_acquired = True
        with states_lock:
            states[i] = "DB_CONCEDIDO"
        print_states()

        # Depois de ter o DB, tenta obter o compilador
        with states_lock:
            states[i] = "ESPERANDO_COMPILADOR"
        print_states()

        compiler_sem.acquire()
        with states_lock:
            states[i] = "COMPILANDO"
        print_states()

        # compilar (segura ambos recursos)
        compile_time = rnd.uniform(1.0, 2.5)
        time.sleep(compile_time)

        # libera compilador e banco
        compiler_sem.release()
        if db_acquired:
            db_sem.release()

        with states_lock:
            states[i] = "LIBEROU_RECURSOS"
        print_states()

        # volta a pensar e o ciclo recomeça
        time.sleep(rnd.uniform(0.5, 1.5))