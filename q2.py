import threading

# A senha correta
senha_correta = "0000000123"

# Número de threads
NUM_THREADS = 4

# Variável global para indicar se a senha já foi encontrada
encontrada = False

# Lock para proteger acesso à variável 'encontrada'
lock = threading.Lock()

def trabalhador(id, inicio, fim):
    global encontrada
    for i in range(inicio, fim):
        with lock:
            if encontrada:
                break  # Outra thread já encontrou a senha

        tentativa = f"{i:010d}"  # Formata o número com 10 dígitos, zeros à esquerda

        if tentativa == senha_correta:
            with lock:
                encontrada = True  # Marca como encontrada
                print(f"Senha encontrada: {tentativa} pela thread #{id}")
            break

def main():
    total_senhas = 10**10
    senhas_por_thread = total_senhas // NUM_THREADS
    threads = []

    for i in range(NUM_THREADS):
        inicio = i * senhas_por_thread
        fim = total_senhas if i == NUM_THREADS - 1 else (i + 1) * senhas_por_thread
        t = threading.Thread(target=trabalhador, args=(i, inicio, fim))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Espera todas as threads terminarem

if __name__ == "__main__":
    main()
