import threading  # Importa a biblioteca para trabalhar com execução simultânea (threads)

SENHA_CORRETA = "0000001234"  # A senha correta que as threads irão tentar encontrar
T = 50  # Define o número de threads (50 threads no total)

senha_encontrada = False  # Variável para saber se a senha já foi encontrada
lock = threading.Lock()  # Um "bloqueio" para garantir que apenas uma thread modifique a variável 'senha_encontrada' por vez

# Função que cada thread vai executar para tentar encontrar a senha
def testar_senhas(thread_id, inicio, fim):
    global senha_encontrada  # Acessa a variável global que indica se a senha foi encontrada
    for num in range(inicio, fim):  # Cada thread tenta uma faixa de números
        if senha_encontrada:  # Se a senha já foi encontrada por outra thread, a função é interrompida
            return

        senha_teste = f"{num:010d}"  # Formata o número para 10 dígitos (com zeros à esquerda)

        if senha_teste == SENHA_CORRETA:  # Verifica se a senha testada é a correta
            with lock:  # Garante que só uma thread pode marcar a senha como encontrada
                senha_encontrada = True  # Marca que a senha foi encontrada
                print(f"Senha encontrada: {senha_teste} pela Thread {thread_id}")  # Exibe a senha e qual thread encontrou
            return  # Termina a execução da thread quando encontra a senha

# Função principal que cria e executa as threads
def main():
    total_senhas = 10**10  # Total de combinações possíveis (10 bilhões, pois a senha tem 10 dígitos)
    senhas_por_thread = total_senhas // T  # Divide as senhas entre as threads de forma equilibrada
    
    threads = []  # Lista para armazenar as threads
    
    for i in range(T):  # Cria e inicia as threads
        inicio = i * senhas_por_thread  # Começo da faixa de senhas para essa thread
        fim = (i + 1) * senhas_por_thread if i != T - 1 else total_senhas  # Fim da faixa de senhas (última thread pega o restante)

        thread = threading.Thread(  # Cria uma nova thread
            target=testar_senhas,  # Define a função que a thread vai executar
            args=(i, inicio, fim))  # Passa os parâmetros para a função
        threads.append(thread)  # Adiciona a thread à lista
        thread.start()  # Inicia a execução da thread
    
    for thread in threads:  # Espera todas as threads terminarem
        thread.join()

# Executa o código quando o script é executado
if __name__ == "__main__":
    main()
