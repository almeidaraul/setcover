#!/usr/bin/python3
import sys
import datetime as dt

nos_visitados = 0
otimo = {
        "atores": [],
        "custo": float("inf")
    }

def custo(atores):
    """
    INPUT:
    * atores: atores já escolhidos
    OUTPUT:
    * custo já obtido
    """
    global v
    return sum([v[ator] for ator in atores])

def bound_1(i, atores):
    """
    INPUT:
    * i: ator atual
    * atores: atores já escolhidos
    OUTPUT:
    * menor custo possível (segundo essa bound)
    """
    return custo(atores)

def bound_2(i, atores):
    """
    INPUT:
    * i: ator atual
    * atores: atores já escolhidos
    OUTPUT:
    * menor custo possível (segundo essa bound)
    """
    global v, n
    custo_atual = custo(atores)
    faltantes = v.copy()[i:]
    faltantes.sort()
    faltantes = faltantes[:n-len(atores)]
    return custo_atual + sum(faltantes)

def verifica_factibilidade(i, atores):
    """
    INPUT:
    * i: ator atualmente contemplado
    * atores: atores ja escolhidos
    OUTPUT:
    * tem soluçoes factiveis (True ou False)
    """
    global grupos, n
    numero_atores = len(grupos)
    if numero_atores <= i and len(atores) < n:
        return False
    contemplados = set()
    for ator in atores:
        for grupo in grupos[ator]:
            contemplados.add(grupo)
    restantes = set()
    for ator in range(i, numero_atores):
        for grupo in grupos[ator]:
            restantes.add(grupo)
    # teste 1: não pode contemplar todos os grupos
    if len(contemplados.union(restantes)) != l:
        return False
    # teste 2: escolheu mais atores do que personagens
    if len(atores) > n:
        return False
    # teste 3: não vai atingir o número suficiente de atores
    if len(atores)+numero_atores-i < n:
        return False
    return True

def solve(i=0, atores=[]):
    """
    INPUT:
    * i: ator atualmente sendo contemplado,
    * atores: atores ja escolhidos

    OUTPUT: None
    """
    global nos_visitados, n, bound
    nos_visitados += 1
    if not verifica_factibilidade(i, atores):
        return
    if len(atores) == n: # já pegou todos os personagens
        custo_atual = custo(atores)
        if otimo["custo"] > custo_atual:
            otimo["atores"] = atores
            otimo["custo"] = custo_atual
        return

    bound_skip = bound(i+1, atores)
    bound_pick = bound(i+1, atores+[i])
    if min(bound_pick, bound_skip) >= otimo["custo"]:
        return
    if bound_pick < bound_skip:
        solve(i+1, atores+[i])
        if bound_skip < otimo["custo"]:
            solve(i+1, atores)
    else:
        solve(i+1, atores)
        if bound_pick < otimo["custo"]:
            solve(i+1, atores+[i])


# entrada
bound = bound_2
if len(sys.argv) > 1 and sys.argv[1] == '-a':
    bound = bound_1
entrada = [int(x) for x in sys.stdin.read().split()]
cursor = 3
l = entrada[0] # numero de grupos sociais
m = entrada[1] # numero de atores
n = entrada[2] # numero de personagens
v = [] # valores de cada ator
grupos = [] # grupos de cada ator
for _ in range(m):
    v.append(entrada[cursor])
    s = entrada[cursor+1]
    g = []
    for i in range(s):
        g.append(entrada[cursor+2+i])
    grupos.append(g)
    cursor += s+2

tempo_inicio = dt.datetime.now()
solve()
tempo_total = dt.datetime.now() - tempo_inicio
if otimo["custo"] == float("inf"):
    print("Inviável")
else:
    print("Número de nós na árvore da solução:", nos_visitados, file=sys.stderr)
    print("Tempo de execução:", tempo_total, file=sys.stderr)
    for ator in otimo["atores"][:-1]:
        print(ator+1, end=' ')
    print(otimo["atores"][-1]+1)
    print(otimo["custo"])
