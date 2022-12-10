from datetime import datetime
from scipy.spatial import distance
import numpy as np
import random
import queue

import argparse
inicio = datetime.now()

parser = argparse.ArgumentParser(
    description='Number of instances: { 2 ^ N | 4 <= N <= 10, N ∊ Z} ')
parser.add_argument('integer', metavar='N', type=int, nargs=1,
                    help='an integer for the instance from 4 (four) to 10 (ten)')
args = parser.parse_args()


class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, b):
        x = self.x - b.x
        y = self.y - b.y
        return Ponto(x, y)

    def __repr__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __lt__(self, other):
        if self.y < other.y:
            return True

        if self.y == other.y and self.x < other.x:
            return True

        return False

    def __eq__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        else:
            return False

    def distEuc(self, other):
        return distance.euclidean([self.x, self.y], [other.x, other.y])

    def distMht(self, other):
        return distance.cityblock([self.x, self.y], [other.x, other.y])


class Grafo:
    def __init__(self, n):
        self.n = n
        self.matrizEuc = np.zeros((n, n), dtype=float)
        self.matrizMhn = np.zeros((n, n), dtype=int)

    def geraMatriz(self, pts):
        for x in range(self.n):
            for y in range(self.n):
                if (x != y):
                    if [self.matrizEuc[x][y] == 0]:
                        dist1 = pts[x].distEuc(pts[y])
                        dist2 = pts[x].distMht(pts[y])
                        self.matrizEuc[x][y] = dist1
                        self.matrizMhn[y][x] = dist2
                else:
                    self.matrizEuc[x][y] = 0
                    self.matrizMhn[x][y] = 0


def geraPts(num):
    pVec = []
    x = 0
    while x < num:
        m = random.randint(0, 2048)
        n = random.randint(0, 2048)

        a = Ponto(m, n)
        if len(pVec) == 0:
            pVec.append(a)
            x += 1
        else:
            if not (any(k == a for k in pVec)):
                pVec.append(a)
                x += 1

    return pVec


def solComplete(n, l):
    aux = np.array(l)
    vertex = np.unique(l)
    return len(vertex) == n


def bound(grafo, l):
    exp_List = []

    for x in range(len(grafo)):
        helper = grafo[x].copy()
        helper.sort()
        exp = [helper[1]] + [helper[2]]
        exp_List.append(exp)

    if len(l) > 1:
        for x in range(len(l)-1):
            exp = grafo[l[x]][l[x+1]]
            if exp_List[l[x]].count(exp) == 0:
                exp_List[l[x]][1] = exp
                if exp_List[l[x+1]].count(exp) == 0:
                    exp_List[l[x+1]][0] = exp

    sum_list = 0
    for x in exp_List:
        sum_list += sum(x)

    if sum_list < 0:
        raise Exception("ERRO: A estimativa nao e' valida!")
    return sum_list/2


def branch_and_bound_tsp(grafo, n):
    #      (Estimativa do no ,  Nivel, Custo, Caminho)
    raiz = (bound(grafo, [0]),      0,     0,     [0])
    fila = queue.PriorityQueue()
    fila.put(raiz)
    best = np.inf
    sol = []
    while not (fila.empty()):
        node = fila.get()
        if node[1] > n:
            if best > node[2]:
                best = node[2]
                sol = (node[3])
        elif node[0] < best:
            if node[1] < n:
                for k in range(1, n+1):
                    if node[3].count(k) == 0 and grafo[node[3][-1]][k] != np.inf and bound(grafo, node[3] + [k]) < best:
                        newSol = node[3] + [k]
                        newBound = bound(grafo, node[3] + [k])
                        newLevel = node[1] + 1
                        newCost = node[2] + grafo[node[3][-1]][k]
                        fila.put((newBound, newLevel, newCost, newSol))

            elif grafo[node[3][-1]][0] != np.inf and bound(grafo, node[3] + [0]) < best and solComplete(len(grafo), node[3]):
                newBound = bound(grafo, node[3] + [0])
                newLevel = node[1] + 1
                newCost = node[2] + grafo[node[3][-1]][0]
                fila.put((newBound, newLevel, newCost, node[3] + [0]))
    return sol, best


print("Algoritimo Branch and Bound")
print("by Henrique Rotsen Santos Ferreira\n")

iTam = args.integer[0]
assert 4 <= iTam and iTam <= 10
print("Tamanho da instancia: 2^%d [%d]" % (iTam, 2**iTam))

pts = geraPts(2**iTam)
grafo = Grafo(len(pts))
grafo.geraMatriz(pts)

# Euclideana
tsp, sum1 = branch_and_bound_tsp(grafo.matrizEuc, grafo.n - 1)
print("\nCaminho do caixeiro:", tsp)
print("Distancia Euclideana:", sum1)

# Manhattan
tsp, sum2 = branch_and_bound_tsp(grafo.matrizMhn, grafo.n - 1)
print("\nCaminho do caixeiro:", tsp)
print("Distancia de Manhattan:", sum2)


print("\nDiferenca entre as distancias:", sum2-sum1)
print("Diferenca entre as distancias em [%]:",
      (sum2/sum1 - 1) * 100, end=" %\n")


fim = datetime.now()
print("\nTempo Total Gasto na Instancia 2^%d [%d]: " % (
    iTam, 2**iTam), fim - inicio)
print("\n----------------------------####################----------------------------", end="")
