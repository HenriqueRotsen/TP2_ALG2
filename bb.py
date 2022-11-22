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

  def distEuc(self, other):
    return distance.euclidean([self.x, self.y], [other.x, other.y])

  def distMht(self, other):
    return distance.cityblock([self.x, self.y], [other.x, other.y])

def geraPts(num):
  pVec = []
  x = 0
  while x < num:
    m = random.randint(0, 2048)
    n = random.randint(0, 2048)
    
    a = Ponto(m, n)
    if len(pVec) == 0:
        pVec.append(a)
    else:
        if not(any(k == a for k in pVec)):
            pVec.append(a)
            x += 1
  return pVec

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
  print(matAdj)
        

inicio = datetime.now()
pts = geraPts(2**1)
criaMatriz(pts)

print("\n---------PONTOS---------\n")
print(pts)
fim = datetime.now()
print("\n\nTempo total gasto: ", fim - inicio)