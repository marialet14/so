import threading  # Importa a biblioteca para trabalhar com threads (execução simultânea)
import time       # Importa a biblioteca para controlar o tempo de espera
import random     # Importa a biblioteca para gerar números aleatórios

NUM_EQUIPES = 2  # Define o número de equipes (2 equipes)
CORREDORES_POR_EQUIPE = 3  # Define o número de corredores por equipe (3 corredores)
NUM_PONTOS = 3  # Define o número de pontos na corrida (3 pontos)

# Criando barreiras para cada equipe e para cada ponto
barreiras = {
    equipe: [threading.Barrier(CORREDORES_POR_EQUIPE) for _ in range(NUM_PONTOS)]  # Cada ponto tem uma barreira para esperar todos os corredores
    for equipe in range(NUM_EQUIPES)  # Cria barreiras para cada equipe
}

# Função principal que organiza a corrida
def main():
    threads = []  # Lista para armazenar as threads (corredores)
    
    # Cria e inicia as threads (corredores) para cada equipe
    for equipe in range(NUM_EQUIPES):
        for corredor_id in range(CORREDORES_POR_EQUIPE):
            t = threading.Thread(target=corredor, args=(equipe, corredor_id))  # Cria a thread para o corredor
            threads.append(t)  # Adiciona a thread à lista
            t.start()  # Inicia a execução da thread (corredor)
            
    for t in threads:  # Aguarda todas as threads (corredores) terminarem
        t.join()
    
    print("Corrida finalizada!")  # Exibe quando todos os corredores terminarem a corrida

# Função que simula a ação de cada corredor
def corredor(equipe_id, corredor_id):
    print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} pronto no ponto A")  # Exibe que o corredor está pronto no ponto A

    # Cada corredor passa por todos os pontos da corrida
    for ponto in range(NUM_PONTOS):
        tempo_corrida = random.uniform(0.5, 2.0)  # Define um tempo aleatório para o corredor chegar no ponto
        time.sleep(tempo_corrida)  # O corredor "corre" por esse tempo

        letra_ponto = chr(66 + ponto)  # Converte o número do ponto (0 -> 'B', 1 -> 'C', etc.)
        print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} chegou ao ponto {letra_ponto}")  # Exibe que o corredor chegou ao ponto

        barreiras[equipe_id][ponto].wait()  # Espera os outros corredores da mesma equipe chegarem no ponto (barreira)

        # Se não for o último ponto, o corredor parte para o próximo ponto
        if ponto < NUM_PONTOS - 1:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} partiu do ponto {letra_ponto}")
        else:
            print(f"Equipe {equipe_id} - Corredor {corredor_id + 1} finalizou a corrida no ponto {letra_ponto}")  # Finaliza a corrida

# Executa o código quando o script é rodado
if __name__ == "__main__":
    main()
