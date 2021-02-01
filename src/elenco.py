import sys
import datetime as dt

def custo(v, atores_escolhidos):
    """
    INPUT:
    * vetor de custos dos atores
    * atores já escolhidos
    OUTPUT:
    * custo já obtido
    """
    return sum([v[ator] for ator in atores_escolhidos])

def bound_original(n, v, i, atores_escolhidos):
    """
    INPUT:
    * numero de personagens
    * vetor de custos dos atores
    * ator atual
    * atores já escolhidos
    OUTPUT:
    * menor custo possível de obter
    """
    custo_atual = custo(v, atores_escolhidos)
    atores_restantes = v[i:].copy()
    atores_restantes.sort()
    return custo_atual + sum(atores_restantes[:n-len(atores_escolhidos)])

def bound_alternativa():
    pass

def verifica_factibilidade(grupos, l, n, i, atores_escolhidos):
    """
    INPUT:
    * grupos: grupos sociais de cada ator
    * l: numero de grupos sociais
    * n: numero de personagens
    * i: ator atualmente contemplado
    * atores_escolhidos: atores ja escolhidos
    OUTPUT:
    * tem soluçoes factiveis (True ou False)
    """
    # testes de corner case da função
    # if numero_atores <= i and len(atores_escolhidos) < n:
    #     return False

    numero_atores = len(grupos)
    contemplados = set([
        grupo for a in atores_escolhidos for grupo in grupos[a]
        ])
    restantes = set([
        grupo for a in range(i, numero_atores) for grupo in grupos[a]
        ])
    # teste 1: não pode contemplar todos os grupos
    if len(contemplados.union(restantes)) != l:
        return False
    # teste 2: escolheu mais atores do que personagens
    if len(atores_escolhidos) > n:
        return False
    # teste 3: não vai atingir o número suficiente de atores
    if len(atores_escolhidos)+numero_atores-i < n:
        return False
    return True

def solve(bound, grupos, v, l, n, i=0, atores_escolhidos=[]):
    """
    INPUT:
    * funçao de bound a ser usada,
    * grupos sociais de cada ator
    * custo de cada ator
    * numero de grupos sociais,
    * numero de personagens,
    * ator atualmente sendo contemplado,
    * atores ja escolhidos

    OUTPUT: (atores escolhidos, custo obtido, i)
        se nao obteve soluçao, retorna ([], -1, i)
    """
    # print("-------------- entrei na solve")
    # print("atores escolhidos:", atores_escolhidos)
    if i == 0:
        ok = verifica_factibilidade(grupos, l, n, i, atores_escolhidos)
        if not ok:
            return ([], -1, i)
    if len(atores_escolhidos) == n: # já pegou todos os personagens
        return (atores_escolhidos, custo(v, atores_escolhidos), i)

    e = bound(n, v, i+1, atores_escolhidos)
    d = bound(n, v, i+1, atores_escolhidos+[i])
    esq_ = verifica_factibilidade(grupos, l, n, i+1, atores_escolhidos)
    dir_ = verifica_factibilidade(grupos, l, n, i+1, atores_escolhidos+[i])
    # print("e: {}, d: {}, esq_: {}, dir_: {}".format(
    #     e, d, esq_, dir_))
    if not (esq_ or dir_):
        return ([], -1, i)
    if e < d:
        if esq_:
            # print("fui pra a esquerda1")
            return solve(bound, grupos, v, l, n, i+1, atores_escolhidos)
        else:
            # print("fui pra a direita1")
            return solve(bound, grupos, v, l, n, i+1, atores_escolhidos+[i])
    else:
        if dir_:
            # print("fui pra a direita2")
            return solve(bound, grupos, v, l, n, i+1, atores_escolhidos+[i])
        else:
            # print("fui pra a esquerda2")
            return solve(bound, grupos, v, l, n, i+1, atores_escolhidos)

# entrada
bound = bound_original
if len(sys.argv) > 1 and sys.argv[1] == '-a':
    bound = bound_alternativa
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
ans = solve(bound, grupos, v, l, n)
tempo_total = dt.datetime.now() - tempo_inicio
nos_visitados = ans[2]
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
