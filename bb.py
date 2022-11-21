import numpy as np
import random
from datetime import datetime
from scipy.spatial import distance

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


def geraPts(n):
  pVec = []
  for x in range(n):
    m = random.randint(0, 2048)
    n = random.randint(0, 2048)
    
    a = Ponto(m,n)
    if len(pVec) == 0:
        pVec.append(a)
    else:
        if not(any(x == a for x in pVec)):
            pVec.append(a)
  return pVec

class ListAdj:
    def __init__(self, p):
        self.p = p

    def __distEuc__(self, p1): 
      return distance.euclidean(self.p, p1)
    
    def __distMht__(self, p1): 
      return distance.cityblock(self.p, p1)



def criaMatriz(pts):
  matAdj = [[]]
  aux = []
  for i in pts:
    for j in pts:
      aux.append(j)
    matAdj.append(aux)
    aux.clear()
  return matAdj



inicio = datetime.now()
x = geraPts(2)
mat = criaMatriz(x)
print(mat)
print(x)





fim = datetime.now()
print("\n\nTempo total gasto: ", fim - inicio)