import threading
import time
import random

NUM_FILOSOFOS = 5
TEMPO_EXECUCAO = 10  # segundos

nomes = ["Sócrates", "Platão", "Aristóteles", "Descartes", "Nietzsche"]

estados = ["pensando"] * NUM_FILOSOFOS
garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
uso_garfos = [None] * NUM_FILOSOFOS  # Indica quem está usando cada garfo
mutex_estado = threading.Lock()

def mostrar_situacao():
    with mutex_estado:
        print("\n📋 Situação atual:")
        for i in range(NUM_FILOSOFOS):
            print(f"{nomes[i]:<12}: {estados[i]}")
        print("\n🍴 Garfos em uso:")
        for i in range(NUM_FILOSOFOS):
            if uso_garfos[i] is not None:
                print(f"Garfo {i + 1}: usado por {nomes[uso_garfos[i]]}")
            else:
                print(f"Garfo {i + 1}: livre")
        print("-" * 40)

def filosofo(id):
    inicio = time.time()
    while time.time() - inicio < TEMPO_EXECUCAO:
        with mutex_estado:
            estados[id] = "pensando"
        print(f"🧠 {nomes[id]} está pensando.")
        time.sleep(random.uniform(0.5, 1.5))

        # Ordem alternada pra evitar deadlock
        if id % 2 == 0:
            primeiro = id
            segundo = (id + 1) % NUM_FILOSOFOS
        else:
            primeiro = (id + 1) % NUM_FILOSOFOS
            segundo = id

        with garfos[primeiro]:
            with garfos[segundo]:
                with mutex_estado:
                    estados[id] = "comendo"
                    uso_garfos[primeiro] = id
                    uso_garfos[segundo] = id

                print(f"🍽️ {nomes[id]} está comendo com os garfos {primeiro + 1} e {segundo + 1}.")
                mostrar_situacao()
                time.sleep(random.uniform(0.5, 1.5))

                with mutex_estado:
                    uso_garfos[primeiro] = None
                    uso_garfos[segundo] = None

    with mutex_estado:
        estados[id] = "terminou"

# Cria as threads
threads = []
for i in range(NUM_FILOSOFOS):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

# Espera o fim
for t in threads:
    t.join()

print("\n📊 Estado final dos filósofos:")
mostrar_situacao()


