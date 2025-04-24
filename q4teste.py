import threading
import time
import random

NUM_FILOSOFOS = 5
TEMPO_EXECUCAO = 10  # segundos

# Lista de nomes dos filósofos
nomes = ["Sócrates", "Platão", "Aristóteles", "Descartes", "Nietzsche"]

estados = ["pensando"] * NUM_FILOSOFOS  # Lista de estados
garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]  # Lista de locks

def filosofo(id):
    inicio = time.time()
    while time.time() - inicio < TEMPO_EXECUCAO:
        # Pensando
        estados[id] = "pensando"
        print(f"🧠 {nomes[id]} está pensando.")
        time.sleep(random.uniform(0.5, 1.5))

        # Decide ordem de pegar os garfos pra evitar deadlock
        if id % 2 == 0:
            primeiro = id
            segundo = (id + 1) % NUM_FILOSOFOS
        else:
            primeiro = (id + 1) % NUM_FILOSOFOS
            segundo = id

        with garfos[primeiro]:
            with garfos[segundo]:
                # Comendo
                estados[id] = "comendo"
                print(f"🍽️ {nomes[id]} está comendo com os garfos {primeiro} e {segundo}.")
                time.sleep(random.uniform(0.5, 1.5))

    estados[id] = "terminou"

# Cria e inicia as threads
threads = []
for i in range(NUM_FILOSOFOS):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

# Espera todas as threads terminarem
for t in threads:
    t.join()

# Estado final
print("\n📊 Estado final dos filósofos:")
for i in range(NUM_FILOSOFOS):
    print(f"{nomes[i]}: {estados[i]}")

