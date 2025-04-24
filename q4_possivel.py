import threading
import time
import random

numero_filosofos = 5
execucao = 10

nomes = ["Sócrates", "Platão", "Aristóteles", "Descartes", "Nietzsche"]

estados = ["pensando"] * numero_filosofos

garfos = [threading.Lock() for _ in range(numero_filosofos)]

uso_garfos = [None] * numero_filosofos  

mutex_estado = threading.Lock()

def mostrar_situacao():
    with mutex_estado:
        for i in range(numero_filosofos):
            print(f"{nomes[i]:<12}: {estados[i]}")

        garfos_usados = []
        for i in range(numero_filosofos):
            if estados[i] == "comendo":
                garfos_usados.append((i + 1, uso_garfos[i]))

        for garfo, filosofo in garfos_usados:
            print(f"{nomes[filosofo]} está comendo com os garfos {garfo} e {garfo + 1}")

        livres = [i + 1 for i in range(numero_filosofos) if uso_garfos[i] is None]
        if livres:
            print(f"Garfo(s) {', '.join(map(str, livres))} livre(s)")

        print("-" * 40)

def filosofo(id):
    inicio = time.time()
    while time.time() - inicio < execucao:
        with mutex_estado:
            estados[id] = "pensando"
        print(f"{nomes[id]} está pensando.")
        time.sleep(random.uniform(0.5, 1.5))

        if id % 2 == 0:
            primeiro = id
            segundo = (id + 1) % numero_filosofos
        else:
            primeiro = (id + 1) % numero_filosofos
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
                    estados[id] = "terminou"

    mostrar_situacao()

threads = []
for i in range(numero_filosofos):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
