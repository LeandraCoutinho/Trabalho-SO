import threading, time
from questao_2.questao_threads import programmer, NUM_PROGRAMMERS, print_states

def run():
    threads = []
    for i in range(NUM_PROGRAMMERS):
        t = threading.Thread(target=programmer, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    try:
        print_states()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando (Ctrl-C recebido).")