import threading
import time
import random

NUM_EQUIPES = 2
CORREDORES_POR_EQUIPE = 3
NUM_PONTOS = 3

barreiras = {
    equipe: [threading.Barrier(CORREDORES_POR_EQUIPE) for _ in range(NUM_PONTOS)] # Criamos uma barreira para cada equipe e para cada ponto
    for equipe in range(NUM_EQUIPES)
}

def main():
    threads = []
    for equipe in range(NUM_EQUIPES):
        for corredor_id in range(CORREDORES_POR_EQUIPE):
            t = threading.Thread(target=corredor, args=(equipe, corredor_id))
            threads.append(t)
            t.start() #Cria a inicia
            
    for t in threads:
        t.join()
    print("Corrida finalizada!")

def corredor(equipe_id, corredor_id):
    print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} pronto no ponto A")

    for ponto in range(NUM_PONTOS):
        tempo_corrida = random.uniform(0.5, 2.0)
        time.sleep(tempo_corrida)

        letra_ponto = chr(66 + ponto)
        print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} chegou ao ponto {letra_ponto}")

        barreiras[equipe_id][ponto].wait() # Espera os outros corredores chegarem e passa pro barrier para determinar a quantidade

        if ponto < NUM_PONTOS - 1:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} partiu do ponto {letra_ponto}")
        else:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} finalizou a corrida no ponto {letra_ponto}")


if __name__ == "__main__":
    main()
