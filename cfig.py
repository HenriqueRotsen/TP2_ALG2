from datetime import datetime
from scipy.spatial import distance
import numpy as np
import random
import scipy as sp
import igraph as ig
import matplotlib.pyplot as plt

import argparse

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


def christofides(grafo):
    gf = ig.Graph.Adjacency(grafo)
    ig.plot(gf, target='myfile.pdf')

    mst = gf.spanning_tree()
    
    i = []
    
    for x in range(1, mst.vcount()):
        print(mst.degree(x, mode='all', loops=False))
        
    
    #aux = gf.induced_subgraph(i)

    #m = aux.minimum_matching()
    #g1 = ig.Graph.Adjacency(mst)
    #g1.add_edges(m)
    #euleriano = g1.dfs(vid=0)
    #return euleriano[0] + [0]


inicio = datetime.now()
print("Algoritimo de Christofides")
print("by Henrique Rotsen Santos Ferreira\n")

iTam = args.integer[0]
assert 0 <= iTam and iTam <= 10
print("Tamanho da instancia: 2^%d [%d]" % (iTam, 2**iTam))

pts = geraPts(2**iTam)
grafo = Grafo(len(pts))
grafo.geraMatriz(pts)

# Euclideana
tsp = christofides(grafo.matrizEuc.tolist())
sum1 = 0
for i in range(len(tsp) - 2):
    sum1 += grafo.matrizEuc[i][i+1]
print("\nCaminho do caixeiro:", tsp)
print("Distancia Euclideana:", sum1)

# Manhattan
tsp = christofides(grafo.matrizMhn.tolist())
sum2 = 0
for i in range(len(tsp) - 2):
    sum2 += grafo.matrizMhn[i][i+1]
print("\nCaminho do caixeiro:", tsp)
print("Distancia de Manhattan:", sum2)


print("\nDiferenca entre as distancias:", sum2-sum1)
print("Diferenca entre as distancias em [%]:",
      (sum2/sum1 - 1) * 100, end=" %\n")


fim = datetime.now()
print("\nTempo Total Gasto na Instancia 2^%d [%d]: " % (
    iTam, 2**iTam), fim - inicio)
print("\n----------------------------####################----------------------------")
