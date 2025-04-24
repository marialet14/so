import threading
from collections import Counter
import time

N = 10  
T = 4  

def contar_palavras_segmento(segmento, contador_local):
    palavras = segmento.split()
    contador_local.update(palavras)

def dividir_texto(texto, partes):
    tamanho = len(texto)
    segmento_len = tamanho // partes
    return [texto[i*segmento_len:(i+1)*segmento_len] for i in range(partes - 1)] + [texto[(partes-1)*segmento_len:]]
#Essa linha retorna uma lista de strings — cada uma representando um segmento do texto.

def main():
    inicio = time.time()

    # Leitura do arquivo
    with open("Você deve implementar um programa q.txt", "r", encoding="utf-8") as f:
        texto = f.read().lower()

    segmentos = dividir_texto(texto, T)
    threads = []
    contadores = [Counter() for _ in range(T)]

    for i in range(T):
        thread = threading.Thread(target=contar_palavras_segmento, args=(segmentos[i], contadores[i]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()     # Esperar todas as threads terminarem
    contador_total = Counter()
    for c in contadores:
        contador_total.update(c) #Junta todos os Counters em um só, somando as contagens

    print(f"\nTop {N} palavras mais frequentes:")
    for palavra, freq in contador_total.most_common(N):
        print(f"{palavra}: {freq}")

    fim = time.time()
    duracao = fim - inicio
    print(f"\nDuração do programa: {duracao:.2f} segundos")

if __name__ == "__main__":
    main()
