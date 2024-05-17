import statistics

try:
    import rmi
except:
    from src import rmi


# original
def retorna_maior_intervalo_original(lista, numero_registros):
    maior_media = 0
    inicio_maior = 0
    fim_maior = 0
    for x in range(len(lista)):
        limite = x + numero_registros
        if limite > len(lista):
            break
        sublista = lista[x:limite]
        media_atual = statistics.mean(sublista)
        if media_atual > maior_media:
            maior_media = media_atual
            inicio_maior = x
            fim_maior = limite - 1
    return float(maior_media), inicio_maior, fim_maior

# usando sum 1 -> (https://ideone.com/69O4nQ)
def retorna_maior_intervalo_sum(lista, numero_registros):
    maior_media = 0
    inicio_maior = 0
    for x in range(len(lista) - numero_registros + 1):
        media_atual = sum(lista[x:x + numero_registros]) / numero_registros
        if media_atual > maior_media:
            maior_media = media_atual
            inicio_maior = x
    return maior_media, inicio_maior, inicio_maior + numero_registros - 1

# usando sum 2
def retorna_maior_intervalo_sum2(lista, numero_registros):
    soma_aux = sum(lista[:numero_registros])
    soma = soma_aux
    inicio_maior = 0
    for x in range(1, len(lista)-numero_registros+1):
        soma_aux = soma_aux - lista[x-1] + lista[x+numero_registros-1]
        if soma_aux > soma:
            inicio_maior = x
            soma = soma_aux
    return soma/numero_registros, inicio_maior, inicio_maior + numero_registros - 1

def retorna_maior_intervalo_original2(lista, numero_registros):
    maior_media = 0
    posicao_maior = 0
    for x in range(len(lista) - numero_registros + 1):
        limite = x + numero_registros
        sublista = lista[x:limite]
        media_atual = sum(sublista) / len(sublista) 
        if media_atual > maior_media:
            maior_media = media_atual
            posicao_maior = x
    return maior_media, posicao_maior, posicao_maior + numero_registros - 1

if __name__ == "__main__":
    import random
    from timeit import timeit
    
    # lista com mil números entre 0 e 299
    rlista = random.choices(range(300), k = 1000)
    
    gera_lista = lambda N: list(range(1, N+1))
    glista = gera_lista(1_000_000)
    glista.reverse()
    
    def compara_resultado_dos_metodos(lista=glista, k=3):
        r1 = retorna_maior_intervalo_original(lista, k)
        r2 = retorna_maior_intervalo_original2(lista, k)
        r3 = retorna_maior_intervalo_sum(lista, k)
        r4 = retorna_maior_intervalo_sum2(lista, k)
        r5 = rmi.retorna_maior_intervalo(lista, k)
        print(r1, r2, r3, r4, r5)
        assert(r1 == r2 == r3 == r4 == r5)

    def exec_timeit(lista_nome: str="glista", k=3, number: int=3):
        # executa n-vezes cada teste
        params = {'number': number, 'globals': globals()}

        # imprime os tempos em segundos (quanto menor, mais rápido)
        fmt = "{:.<12} {}".format
        print(fmt('original', timeit(f'retorna_maior_intervalo_original({lista_nome}, {k})', **params)))
        print(fmt('original2', timeit(f'retorna_maior_intervalo_original2({lista_nome}, {k})', **params)))
        print(fmt('sum', timeit(f'retorna_maior_intervalo_sum({lista_nome}, {k})', **params)))
        print(fmt('sum2', timeit(f'retorna_maior_intervalo_sum2({lista_nome}, {k})', **params)))
        print(fmt('cpython', timeit(f'rmi.retorna_maior_intervalo({lista_nome}, {k})', **params)))
    
    # exec_timeit("glista", "3", 10)
    compara_resultado_dos_metodos(rlista)
    
    
