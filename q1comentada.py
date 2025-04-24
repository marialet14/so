import threading  # Importa o módulo para trabalhar com threads (execução paralela)
from collections import Counter  # Importa Counter, que conta elementos (palavras, números, etc.)
import time  # Importa para medir o tempo de execução do programa

N = 10  # Número de palavras mais frequentes que queremos exibir
T = 4   # Número de threads (e de partes que o texto será dividido)

# Função que recebe um pedaço do texto (segmento) e um contador local
def contar_palavras_segmento(segmento, contador_local):
    palavras = segmento.split()  # Divide o segmento em palavras usando espaços como separador
    contador_local.update(palavras)  # Conta cada palavra e atualiza o contador local

# Função que divide o texto igualmente entre as threads
def dividir_texto(texto, partes):
    tamanho = len(texto)  # Pega o tamanho total do texto (em caracteres)
    segmento_len = tamanho // partes  # Calcula o tamanho de cada parte (quociente da divisão inteira)
    # Retorna uma lista de partes do texto (as T-1 primeiras partes são iguais, a última pega o resto)
    return [texto[i*segmento_len:(i+1)*segmento_len] for i in range(partes - 1)] + [texto[(partes-1)*segmento_len:]]

# Função principal do programa
def main():
    inicio = time.time()  # Marca o horário de início da execução do programa

    # Abre o arquivo de texto em modo leitura com codificação UTF-8
    with open("Você deve implementar um programa q.txt", "r", encoding="utf-8") as f:
        texto = f.read().lower()  # Lê todo o conteúdo do arquivo e transforma em minúsculas

    segmentos = dividir_texto(texto, T)  # Divide o texto em T partes

    threads = []  # Lista para armazenar as threads
    contadores = [Counter() for _ in range(T)]  # Cria uma lista com um contador para cada thread

    # Cria e inicia as threads
    for i in range(T):
        # Cria uma thread que chama a função contar_palavras_segmento com os argumentos certos
        thread = threading.Thread(target=contar_palavras_segmento, args=(segmentos[i], contadores[i]))
        threads.append(thread)  # Adiciona a thread à lista
        thread.start()  # Inicia a thread

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()  # Espera a thread atual terminar

    contador_total = Counter()  # Cria um contador para armazenar o total de todas as palavras

    # Junta os contadores locais em um único contador total
    for c in contadores:
        contador_total.update(c)  # Atualiza o contador total com os dados de cada contador local

    # Exibe as N palavras mais frequentes com suas contagens
    print(f"\nTop {N} palavras mais frequentes:")
    for palavra, freq in contador_total.most_common(N):  # Pega as N palavras mais comuns
        print(f"{palavra}: {freq}")  # Imprime a palavra e sua frequência

    fim = time.time()  # Marca o tempo final
    duracao = fim - inicio  # Calcula a duração do programa
    print(f"\nDuração do programa: {duracao:.2f} segundos")  # Mostra quanto tempo demorou

# Garante que a função main só seja executada se o arquivo for rodado diretamente (não importado)
if __name__ == "__main__":
    main()
