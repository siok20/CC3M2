from scipy.optimize import linprog

# Coeficientes de la función objetivo (beneficios de cada mueble)
c = [-50, -40, -70, -60]  # Negativos porque linprog minimiza

# Coeficientes de las restricciones
# Restricciones: tiempo de trabajo, madera, y espacio en almacén
A = [
    [2, 1, 3, 4],  # Tiempo de trabajo
    [3, 2, 4, 3],  # Madera
    [1, 1, 2, 1]   # Espacio en almacén
]

# Límites de cada restricción
b = [200, 300, 150]

# Resolver el problema usando el método 'highs'
res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='revised simplex')

# Resultados
valor_optimo = -res.fun  # Invertir el signo para reflejar la maximización
valores_variables = res.x

print("Valor optimo:", valor_optimo)
print("Valores de las variables:", valores_variables)
