import threading  # Importa a biblioteca para trabalhar com threads (execução simultânea)
import time       # Importa a biblioteca para controlar o tempo de espera
import random     # Importa a biblioteca para gerar números aleatórios

numero_filosofos = 5  # Define que haverá 5 filósofos
execucao = 10  # Define o tempo que o programa vai rodar, em segundos

# Lista com os nomes dos filósofos
nomes = ["Sócrates", "Platão", "Aristóteles", "Descartes", "Nietzsche"]

# Lista que armazena o estado de cada filósofo (pensando inicialmente)
estados = ["pensando"] * numero_filosofos

# Lista de garfos, representados por bloqueios (locks) para garantir acesso exclusivo
garfos = [threading.Lock() for _ in range(numero_filosofos)]

# Lista para verificar qual filósofo está usando cada garfo (inicialmente todos estão livres)
uso_garfos = [None] * numero_filosofos  

# Mutex para garantir que apenas um filósofo acesse os estados ao mesmo tempo
mutex_estado = threading.Lock()

# Função para mostrar a situação atual dos filósofos e dos garfos
def mostrar_situacao():
    with mutex_estado:  # Garante que apenas um filósofo possa acessar a situação por vez
        # Mostrar o estado atual de cada filósofo
        for i in range(numero_filosofos):
            print(f"{nomes[i]:<12}: {estados[i]}")

        # Mostrar quais filósofos estão comendo e quais garfos estão sendo usados
        garfos_usados = []  # Lista para armazenar os filósofos comendo e os garfos que estão usando
        for i in range(numero_filosofos):
            if estados[i] == "comendo":  # Se o filósofo está comendo
                garfos_usados.append((i + 1, uso_garfos[i]))  # Adiciona o filósofo e os garfos que ele está usando

        # Exibe a informação de quem está comendo e quais garfos estão sendo usados
        for garfo, filosofo in garfos_usados:
            print(f"🍽️ {nomes[filosofo]} está comendo com os garfos {garfo} e {garfo + 1}")

        # Mostrar quais garfos estão livres (não sendo usados por nenhum filósofo)
        livres = [i + 1 for i in range(numero_filosofos) if uso_garfos[i] is None]
        if livres:  # Se houver garfos livres
            print(f"🍴 Garfo(s) {', '.join(map(str, livres))} livre(s)")

        print("-" * 40)  # Linha de separação visual

# Função que simula a ação de cada filósofo
def filosofo(id):
    inicio = time.time()  # Marca o tempo de início
    while time.time() - inicio < execucao:  # Executa enquanto o tempo não passar do limite
        with mutex_estado:  # Garante que apenas um filósofo acesse o estado ao mesmo tempo
            estados[id] = "pensando"  # Marca o filósofo como pensando
        print(f"🧠 {nomes[id]} está pensando.")  # Exibe que o filósofo está pensando
        time.sleep(random.uniform(0.5, 1.5))  # O filósofo pensa por um tempo aleatório

        # Decide a ordem dos garfos para evitar deadlock
        if id % 2 == 0:  # Se o id do filósofo for par
            primeiro = id
            segundo = (id + 1) % numero_filosofos  # O segundo garfo será o próximo filósofo
        else:  # Se o id for ímpar
            primeiro = (id + 1) % numero_filosofos
            segundo = id  # O segundo garfo será o filósofo atual

        # Tenta pegar os garfos (garante que o filósofo pega garfos exclusivos)
        with garfos[primeiro]:
            with garfos[segundo]:
                with mutex_estado:  # Garante que apenas um filósofo acesse o estado ao mesmo tempo
                    estados[id] = "comendo"  # Marca o filósofo como comendo
                    uso_garfos[primeiro] = id  # Marca que o primeiro garfo está sendo usado pelo filósofo
                    uso_garfos[segundo] = id   # Marca que o segundo garfo está sendo usado pelo filósofo

                # Exibe que o filósofo está comendo com os garfos que pegou
                print(f"🍽️ {nomes[id]} está comendo com os garfos {primeiro + 1} e {segundo + 1}.")
                mostrar_situacao()  # Exibe a situação atual após o filósofo começar a comer
                time.sleep(random.uniform(0.5, 1.5))  # O filósofo come por um tempo aleatório

                # Libera os garfos após o filósofo terminar de comer
                with mutex_estado:
                    uso_garfos[primeiro] = None  # Libera o primeiro garfo
                    uso_garfos[segundo] = None   # Libera o segundo garfo
                    estados[id] = "terminou"  # Marca que o filósofo terminou de comer

    # Exibe a situação final após o filósofo terminar
    mostrar_situacao()

# Cria uma lista de threads (uma para cada filósofo)
threads = []
for i in range(numero_filosofos):
    t = threading.Thread(target=filosofo, args=(i,))  # Cria uma thread para cada filósofo
    threads.append(t)
    t.start()  # Inicia a execução da thread

# Espera todas as threads terminarem
for t in threads:
    t.join()

