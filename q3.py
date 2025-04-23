import threading
import time
import random

# === Constantes ===
EQUIPES = 2
CORREDORES_POR_EQUIPE = 3
PONTOS = 3  # Ponto B, C, D (se for 1: só B, se 2: B e C, etc.)

# === Criação das barreiras ===
# Um dicionário onde cada equipe tem uma lista de barreiras
barreiras = {
    equipe: [threading.Barrier(CORREDORES_POR_EQUIPE) for _ in range(PONTOS)]
    for equipe in range(EQUIPES)
}

# === Função que simula um corredor ===
def corredor(equipe_id, corredor_id):
    print(f"Equipe {equipe_id} - Corredor {corredor_id} pronto para largar.")
    time.sleep(random.uniform(0.5, 1.5))  # Preparação diferente por corredor
    print(f" Equipe {equipe_id} - Corredor {corredor_id} largou!")

    for ponto in range(PONTOS):
        tempo = random.uniform(1.0, 3.0)
        time.sleep(tempo)
        letra_ponto = chr(66 + ponto)  # Ponto B, C, D...
        print(f" Equipe {equipe_id} - Corredor {corredor_id} chegou ao Ponto {letra_ponto} (após {tempo:.2f}s). Esperando os outros...")

        barreiras[equipe_id][ponto].wait()

        print(f"Equipe {equipe_id} - Corredor {corredor_id} saindo do Ponto {letra_ponto} com a equipe.")

    print(f"Equipe {equipe_id} - Corredor {corredor_id} chegou ao final da corrida!")

# === Criar e iniciar as threads dos corredores ===
threads = []
for equipe in range(EQUIPES):
    for corredor in range(CORREDORES_POR_EQUIPE):
        t = threading.Thread(target=corredor, args=(equipe, corredor))
        threads.append(t)
        t.start()

# === Aguardar todas as threads terminarem ===
for t in threads:
    t.join()

print("\nCorrida de revezamento finalizada!")
