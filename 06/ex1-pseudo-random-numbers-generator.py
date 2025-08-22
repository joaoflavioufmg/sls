import numpy as np
import matplotlib.pyplot as plt

N = 100
# N = 10000

#######################################################
# Geração de números aleatórios: Exemplo 1 (Pidd)
#######################################################
x0 = [1578, 5135]
y = []
x = []
for i in range(len(x0)):
    y.append(x0[i])

for i in range(2, N):
    y.append(((19031*y[i-1] + 9298*y[i-2]) % 65536))
    x.append(y[i])
    
# print("y: ", y)
# print("x: ", x)

y = y[:-2]
myInt = 65536
yu = [i / myInt for i in y]
xu = [i / myInt for i in x]

fig, ax = plt.subplots()
ax.set_title(f'Geração de números aleatórios ({N} dados): Exemplo 1 (Pidd)')
ax.grid(True)
fig.tight_layout()
plt.scatter(xu, yu, alpha=0.5)
plt.show()

#######################################################
# Geração de números aleatórios: Exemplo 2 (Pidd)
#######################################################
x0 = [1578]
y = []
x = []
for i in range(len(x0)):
    y.append(x0[i])

for i in range(1, N):
    y.append((16807*y[i-1]) % (pow(2,31)-1))
    x.append(y[i])
    
y = y[:-1]

# print("y: ", y)
# print("x: ", x)

myInt = pow(2,31)-1
yu = [i / myInt for i in y]
xu = [i / myInt for i in x]

fig, ax = plt.subplots()
ax.set_title(f'Geração de números aleatórios ({N} dados): Exemplo 2 (Pidd)')
ax.grid(True)
fig.tight_layout()
plt.scatter(xu, yu, alpha=0.5)
plt.show()


##########################################################
# Geração de números aleatórios: Biblioteca Numpy (Python)
##########################################################

# Fixando o estado random para reprodutibilidade
np.random.seed(1)

x = np.random.rand(N)
y = np.random.rand(N)

# print("y: ", y)
# print("x: ", x)

fig, ax = plt.subplots()
ax.set_title(f'Geração de números aleatórios ({N} dados): Biblioteca Numpy (Python)')
ax.grid(True)
fig.tight_layout()
plt.scatter(x, y, alpha=0.5)
plt.show()