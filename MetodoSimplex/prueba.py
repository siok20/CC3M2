import numpy as np

A = np.array([[  2. ,  1.,   3.,   4.,   1.,   0.,   0., 200.],
 [  3.  , 2.  , 4. ,  3.  , 0.  , 1. ,  0., 300.],
 [  1.  , 1. ,  2.,   1. ,  0. ,  0. ,  1., 150.],
 [-50., -40., -70. ,-60.,   0.  , 0.,   0. ,  0.]])

# Primera parte: encontrar el índice `j` de un elemento negativo mínimo en la última fila
i, j = np.inf, 0  # Usamos np.inf para iniciar `i` con un valor grande

for t, n in enumerate(A[-1]):  # Recorremos la última fila
    if n < 0 and n < i:  # Si encontramos un valor negativo menor que `i`
        j = t            # Guardamos el índice de columna
        i = n            # Guardamos el valor

# Segunda parte: encontrar el índice `i` con el menor ratio `n / A[t][j]` en la columna `j`
l = np.inf  # Inicializamos l con infinito positivo
i = 0       # Inicializamos el índice i

for t, n in enumerate(A[:, -1]):  # Recorremos la última columna
    if A[t][j] == 0:  # Si el elemento en la columna `j` es 0
        i = t         # Guardamos el índice y rompemos el ciclo
        break
    elif A[t][j] > 0:  # Solo consideramos divisiones positivas
        ratio = n / A[t][j]
        if ratio < l:  # Buscamos la menor razón
            l = ratio
            i = t
print(A[i][j])
piv = A[i][j]
fil_piv = A[i]

fil_piv /= piv

for k in range(len(A)):
    if k != i:  # Evitamos la fila pivote
        A[k] = A[k] - A[k][j] * A[i]
for i in range(A.shape[0]):      # Recorre cada fila
    for j in range(A.shape[1]):  # Recorre cada columna
        print(f"Elemento en ({i}, {j}):", A[i, j])

print(A)
print("Índice de columna (j) con el valor negativo mínimo en la última fila:", j)
print("Índice de fila (i) con el menor ratio en la columna", j, ":", i)