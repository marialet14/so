import threading
import time
import random

numero_equipes = 2
corredores_equipe = 3
num_pontos = 3

barreiras = {
    equipe: [threading.Barrier(corredores_equipe) for _ in range(num_pontos)] 
    for equipe in range(numero_equipes)
}

def main():
    threads = []
    for equipe in range(numero_equipes):
        for corredor_id in range(corredores_equipe):
            t = threading.Thread(target=corredor, args=(equipe, corredor_id))
            threads.append(t)
            t.start() 
            
    for t in threads:
        t.join()
    print("Corrida finalizada!")

def corredor(equipe_id, corredor_id):
    print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} pronto no ponto A")

    for ponto in range(num_pontos):
        tempo_corrida = random.uniform(0.5, 2.0)
        time.sleep(tempo_corrida)

        letra_ponto = chr(66 + ponto)
        print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} chegou ao ponto {letra_ponto}")

        barreiras[equipe_id][ponto].wait() 

        if ponto < num_pontos - 1:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} partiu do ponto {letra_ponto}")
        else:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} finalizou a corrida no ponto {letra_ponto}")


if __name__ == "__main__":
    main()
