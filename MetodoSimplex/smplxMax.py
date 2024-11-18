import numpy as np

def isValid(z):
    return np.any(z<0)

def pivote(A,z):
    i, j = np.inf, 0

    j = np.argmin(z[:-1, 0] + 1e6 * z[:-1, 1])
    l = np.inf
    i = 0

    for t, n in enumerate(A[:, -1]):
        if A[t][j] > 0:
            ratio = n / A[t][j]
            if ratio < l:
                l = ratio
                i = t

    return i, j

def display_tabla(A, num_vars, num_holguras, num_artificiales,M ,decimales=2):
    encabezado = ""
    for i in range(num_vars):
        encabezado += f"\tx{i+1}"
    for i in range(num_holguras):
        encabezado += f"\ts{i+1}"
    for i in range(num_artificiales):
        encabezado += f"\tA{i+1}"
    encabezado += "\tr"  
    print(encabezado)
    
    formato = f"{{:.{decimales}f}}"  

    for i in range(A.shape[0]): 
        fila = ""
        for j in range(A.shape[1]):  
            fila += "\t" + formato.format(A[i, j]) 
        print(fila)

def display_M(c, ):
    print("c: ", end="\t")
    
    for i, fila in enumerate(c):
        for j, elemento in enumerate(fila):
            if elemento == 0 and j == 1:
                continue
            if j == 0:
                print(f"{elemento:.2f}", end=" ") 
            else:
                print(f"{elemento:.2f}M", end=" ")

        print("\t",end="")
    print()

def met_simplex_M(obj, c, A, b, M=1e6):

    num_vars = len(c)
    num_restr = len(b)

    holguras = np.eye(num_restr)   
    num_artificiales = 0
    artificiales = []
    for i, item in enumerate(b):
        if item <=0:
            holguras[i][i] *=-1
            num_artificiales+=1

    for i, item in enumerate(b):
        if item >0:
            artificiales.append(np.zeros(num_artificiales))
        else:
            artificiales.append(np.eye(num_artificiales)[i%num_artificiales])

    artificiales = np.array(artificiales)

    A = np.hstack((A, holguras, artificiales)) 

    c_new = []

    for i in range(len(c)):
        c_new.append([c[i],0])

    for _ in range(num_restr):
        c_new.append([0,0])

    for _ in range(num_artificiales):
        c_new.append([0,-1])
    
    c = np.array(c_new, dtype=float)
    
    A = np.hstack((A, np.abs(np.array(b)).reshape(-1, 1)))  
    cb = []
    t=[]

    for i in range(num_restr):
        if A[i,num_vars+i] == 1:
            t.append(num_vars+i)
        else:
            t.append(num_vars+i%num_artificiales +num_restr)
    
    indices = t.copy()
    cb = np.copy(c)
    cb = np.append(cb,[[0,0]], axis=0)
    
    z = np.copy(c) * -1
    z = np.append(z,[[0,0]], axis=0)
    
    for i, fila in enumerate(A):
        for j, elemento in enumerate(fila):
            z[j] += elemento*cb[indices[i]]
    
    q = 0
    zj = np.copy(z)

    while isValid(zj):
        print("="*100)
        print(f'Iteracion {q+1}')
        display_M(c)
        display_tabla(A, num_vars, num_restr, num_artificiales, M)
        display_M(zj)
        i, j = pivote(A, zj)
        print(f"Pivote en fila {i}, columna {j}")
        indices[i] = j
        piv = A[i][j]
        if piv == 0:
            print("Error: pivote igual a cero, no se puede continuar.")
            break
        A[i] = A[i] / piv  

        for k in range(len(A)):
            if k != i:
                A[k] = A[k] - A[k][j] * A[i]
        zj = np.zeros_like(z)
        for i, fila in enumerate(A):
            for j, elemento in enumerate(fila):
                zj[j] += elemento*cb[indices[i]] 
        zj -= cb
        display_tabla(A, num_vars, num_restr, num_artificiales, M)
        display_M(zj)
        q += 1

    print("="*100)
    print("FINAL")
    display_tabla(A, num_vars, num_restr, num_artificiales,M)
    display_M(zj)

    # Extraer solución
    solution = np.zeros(num_vars)
    for i, item in enumerate(indices):
        if item in range(num_vars):
            solution[item] = A[i,-1]
    return solution, zj[-1][0]

obj = "maximizar"
c = [5, 4]

A = [[2, 1], 
     [1, 1], 
     [1, 2]]

b = [20, -18, -12]

solution, z_value = met_simplex_M(obj, c, np.array(A), np.array(b))
print("\nSolución óptima:")
print("x =", solution)
print("Valor óptimo de z =", z_value)
