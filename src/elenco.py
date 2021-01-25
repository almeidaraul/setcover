import sys
import datetime as dt

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
    custo = sum([v[ator] for ator in atores_escolhidos])
    atores_restantes = v[i:].copy()
    atores_restantes.sort()
    return custo + sum(atores_restantes[:n-len(atores_escolhidos)])

def bound_alternativa():
    pass

def verifica_factibilidade(grupos, l, n, i, atores_escolhidos):
    """
    INPUT:
    * grupos sociais de cada ator
    * numero de grupos sociais
    * numero de personagens
    * ator atualmente contemplado
    * atores ja escolhidos
    OUTPUT:
    * tem soluçoes factiveis (True ou False)
    """
    numero_atores = len(grupos)
    if len(atores_escolhidos) > numero_atores:
        # print("lenatoresescolhidos>=numatores")
        return False
    if numero_atores <= i and len(atores_escolhidos) < n:
        # print("numatores<=i")
        # print("atores_escolhidos: ", atores_escolhidos)
        return False
    grupos_contemplados = set([
        grupo for a in atores_escolhidos for grupo in grupos[a]
        ])
    grupos_restantes = set([
        grupo for a in range(i, numero_atores) for grupo in grupos[a]
        ])
    # print("i: ", i)
    # print("contemplados: ", grupos_contemplados)
    # print("restantes: ", grupos_restantes)
    # print("faltam: ", grupos_restantes - grupos_contemplados)
    # print("")
    if len(grupos_contemplados.union(grupos_restantes)) != l:
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
    ok = verifica_factibilidade(grupos, l, n, i, atores_escolhidos)
    if not ok:
        return ([], -1, i)
    if len(atores_escolhidos) == n: # já pegou todos os personagens
        return (atores_escolhidos, bound(n, v, i, atores_escolhidos), i)

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
