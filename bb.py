from datetime import datetime
from scipy.spatial import distance
import numpy as np
import random
import math
import scipy as sp
import queue
import igraph as ig


import argparse

parser = argparse.ArgumentParser(description='Number of instances: { 2 ^ N | 4 <= N <= 10, N ∊ Z} ')
parser.add_argument('integer', metavar='N', type=int, nargs=1,
                    help='an integer for the instance from 4 (four) to 10 (ten)')
args = parser.parse_args()

class Ponto:
  def __init__(self,x,y):
    self.x = x
    self.y = y

  def __sub__(self,b):
    x = self.x - b.x
    y = self.y - b.y
    return Ponto(x,y)

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
  def __init__(self, tipo, n):
    self.tipo = tipo
    self.n = n
    self.matriz = np.zeros((n, n), dtype=[('state', int), ('value', float)])
    
  def geraMatriz(self, pts):
    for x in range(self.n):    
      for y in range(self.n):
        if(x != y):
          if[self.matriz[x][y][0] == 0]:
            
            if self.tipo == "Euclideana": 
              dist = pts[x].distEuc(pts[y])
            elif self.tipo == "Manhattan": 
              dist = pts[x].distMht(pts[y])
            else:
              raise Exception("O tipo da distancia tem que ser:\nEuclideana\nOU\nManhattan\n")
            
            self.matriz[x][y][1] = dist
            self.matriz[y][x][1] = dist
            
        else:
          self.matriz[x][y] = 0    


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
        if not(any(k == a for k in pVec)):
            pVec.append(a)
            x += 1

  return pVec

'''
def criaMatriz(pts):
  num = len(pts)
  matAdj = np.zeros((num,num),dtype=[('w', 'int'), ('x', 'int'), ('y', 'float'), ('z', 'int')])
  
  for x in range(num):    
    for y in range(num):
      if(x != y):
        if[matAdj[x][y][0] == 0]:
          dE = pts[x].distEuc(pts[y])
          dM = pts[x].distMht(pts[y])
          tupAux = (pts[y].x, pts[y].y, dE, dM)
          tupAux2 = (pts[x].x, pts[x].y, dE, dM)
          matAdj[x][y] = tupAux
          matAdj[y][x] = tupAux2
      else:
        matAdj[x][y] = (pts[x].x, pts[x].y, 0, 0)
  return matAdj
'''


def bnb_tsp(grafo):

  
  fila = queue.Queue()
  best = math.inf
  sol = []

  while not(fila.empty()):
    node = fila.get()




        

inicio = datetime.now()

pts = geraPts(2**4)
pts.sort()

grafo = Grafo("Euclideana", len(pts))
grafo.geraMatriz(pts)
print(grafo.matriz)



fim = datetime.now()
print("\n\nTempo total gasto: ", fim - inicio)