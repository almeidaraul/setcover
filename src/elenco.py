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
    return sum([v[ator] for ator in atores])

def bound_1(n, i, atores):
    """
    INPUT:
    * n: numero de personagens
    * i: ator atual
    * atores: atores já escolhidos
    OUTPUT:
    * menor custo possível (segundo essa bound)
    """
    return custo(atores)

def bound_2(n, i, atores):
    """
    INPUT:
    * n: numero de personagens
    * i: ator atual
    * atores: atores já escolhidos
    OUTPUT:
    * menor custo possível (segundo essa bound)
    """
    custo_atual = custo(atores)
    faltantes = v.copy().sort()[:n-i]
    return custo_atual + custo(faltantes)

def verifica_factibilidade(grupos, l, n, i, atores):
    """
    INPUT:
    * grupos: grupos sociais de cada ator
    * l: numero de grupos sociais
    * n: numero de personagens
    * i: ator atualmente contemplado
    * atores: atores ja escolhidos
    OUTPUT:
    * tem soluçoes factiveis (True ou False)
    """
    # testes de corner case da função
    # if numero_atores <= i and len(atores_escolhidos) < n:
    #     return False

    numero_atores = len(grupos)
    contemplados = set([
        grupo for a in atores for grupo in grupos[a]
        ])
    restantes = set([
        grupo for a in range(i, numero_atores) for grupo in grupos[a]
        ])
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

def solve(grupos, l, n, i=0, atores=[]):
    """
    INPUT:
    * grupos: grupos sociais de cada ator
    * l: numero de grupos sociais,
    * n: numero de personagens,
    * i: ator atualmente sendo contemplado,
    * atores: atores ja escolhidos

    OUTPUT: None
    """
    if not verifica_factibilidade(
            grupos, l, n, i, atores):
        return
    if len(atores) == n: # já pegou todos os personagens
        custo_atual = custo(atores)
        if otimo["custo"] > custo_atual:
            otimo["atores"] = atores
            otimo["custo"] = custo_atual
        return

    bound_skip = bound(n, i+1, atores)
    bound_pick = bound(n, i+1, atores+[i])
    if min(bound_pick, bound_skip) >= otimo["custo"]:
        return
    if bound_pick < bound_skip:
        solve(grupos, l, n, i, atores+[i])
        if bound_skip < otimo["custo"]:
            solve(grupos, l, n, i, atores)
    else:
        solve(grupos, l, n, i, atores)
        if bound_pick < otimo["custo"]:
            solve(grupos, l, n, i, atores+[i])

# entrada
bound = bound_1
if len(sys.argv) > 1 and sys.argv[1] == '-a':
    bound = bound_2
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

# print({
#     'l': l,
#     'm': m,
#     'n': n,
#     'v': v,
#     'grupos': grupos
#     })

tempo_inicio = dt.datetime.now()
ans = solve(grupos, l, n)
tempo_total = dt.datetime.now() - tempo_inicio
# print(ans)
if (ans[1] == -1):
    print("Inviável")
else:
    print("Número de nós na árvore da solução:", ans[2], file=sys.stderr)
    print("Tempo de execução:", tempo_total, file=sys.stderr)
    for ator in ans[0][:-1]:
        print(ator+1, end=' ')
    print(ans[0][-1]+1)
    print(ans[1])
