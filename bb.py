import numpy as np
import random
from datetime import datetime

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

class MatrizAdj:
    def __init__(self, n):
        self.n = n

    def __repr__(self): 
        return "(% s, % s, % s)" % (self.pontoEsquerdo, self.pontoDireito,self.chave)



inicio = datetime.now()
x = geraPts(1024)
print(x)
fim = datetime.now()
print("\n\nTempo total gasto: ", fim - inicio)