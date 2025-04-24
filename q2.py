import threading

SENHA_CORRETA = "0000001234"  
T = 50 

senha_encontrada = False
lock = threading.Lock()

def testar_senhas(thread_id, inicio, fim):
    global senha_encontrada
    for num in range(inicio, fim):
        
        if senha_encontrada:
            return
 
        senha_teste = f"{num:010d}"

        if senha_teste == SENHA_CORRETA:
            with lock: 
                senha_encontrada = True
                print(f"Senha encontrada: {senha_teste} pela Thread {thread_id}")
            return

def main():
    total_senhas = 10**10 
    senhas_por_thread = total_senhas // T
    
    threads = []
    
    for i in range(T):
        inicio = i * senhas_por_thread
        fim = (i + 1) * senhas_por_thread if i != T - 1 else total_senhas
        
        thread = threading.Thread( 
            target=testar_senhas,
            args=(i, inicio, fim))
        threads.append(thread)
        thread.start()
    
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
