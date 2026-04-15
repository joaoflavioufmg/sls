# teste 

import random

taxa = 5 # 5/min   --> a cada 0.2 minutos chega alguém
intervalo = 0.2  # --> a cada 0.2 minutos chega alguém

for i in range(10):
    print(f"Resultado[{i}]:", random.expovariate(intervalo))