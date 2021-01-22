import sys

def bound_original():
    pass

def bound_alternativa():
    pass

def solve(grupos, v, l, n):
    pass

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

print({
    'l': l,
    'm': m,
    'n': n,
    'v': v,
    'grupos': grupos
    })

print(solve(grupos, v, l, n))
