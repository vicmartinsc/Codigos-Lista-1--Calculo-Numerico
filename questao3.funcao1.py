import numpy as np
import matplotlib.pyplot as plt
import time
import math

# ==========================================================
# FUNÇÃO E DERIVADA
# ==========================================================

def f(x):
    return math.cos(x) - x

def df(x):
    return -math.sin(x) - 1

# Forma de ponto fixo: x = cos(x)
def g(x):
    return math.cos(x)


# ==========================================================
# TRUNCAMENTO
# ==========================================================

def trunc4(x):
    return np.trunc(x * 10000) / 10000


# ==========================================================
# BISSECÇÃO
# ==========================================================

def bisseccao(f, a, b, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    if tipo == "float32":
        a, b, tol = np.float32(a), np.float32(b), np.float32(tol)

    for i in range(max_iter):
        if tipo == "float32":
            m = np.float32((a + b)/2)
        elif tipo == "trunc":
            m = trunc4((a + b)/2)
        else:
            m = (a + b)/2

        erro = abs(f(m))
        erros.append(erro)

        if erro < tol:
            break

        if f(a)*f(m) < 0:
            b = m
        else:
            a = m

    return m, i+1, time.time()-inicio, erros


# ==========================================================
# FALSA POSIÇÃO
# ==========================================================

def falsa_posicao(f, a, b, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    if tipo == "float32":
        a, b, tol = np.float32(a), np.float32(b), np.float32(tol)

    for i in range(max_iter):
        fa, fb = f(a), f(b)

        if tipo == "float32":
            m = np.float32((a*fb - b*fa)/(fb-fa))
        elif tipo == "trunc":
            m = trunc4((a*fb - b*fa)/(fb-fa))
        else:
            m = (a*fb - b*fa)/(fb-fa)

        erro = abs(f(m))
        erros.append(erro)

        if erro < tol:
            break

        if fa*f(m) < 0:
            b = m
        else:
            a = m

    return m, i+1, time.time()-inicio, erros


# ==========================================================
# ILLINOIS
# ==========================================================

def illinois(f, a, b, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    if tipo == "float32":
        a, b, tol = np.float32(a), np.float32(b), np.float32(tol)

    fa, fb = f(a), f(b)

    for i in range(max_iter):
        if tipo == "float32":
            m = np.float32((a*fb - b*fa)/(fb-fa))
        elif tipo == "trunc":
            m = trunc4((a*fb - b*fa)/(fb-fa))
        else:
            m = (a*fb - b*fa)/(fb-fa)

        fm = f(m)
        erro = abs(fm)
        erros.append(erro)

        if erro < tol:
            break

        if fa*fm < 0:
            b, fb = m, fm
            fa = fa/2
        else:
            a, fa = m, fm
            fb = fb/2

    return m, i+1, time.time()-inicio, erros


# ==========================================================
# NEWTON
# ==========================================================

def newton(f, df, x0, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    x = np.float32(x0) if tipo=="float32" else x0

    for i in range(max_iter):
        fx, dfx = f(x), df(x)

        if dfx == 0:
            break

        if tipo == "float32":
            x_novo = np.float32(x - fx/dfx)
        elif tipo == "trunc":
            x_novo = trunc4(x - fx/dfx)
        else:
            x_novo = x - fx/dfx

        erro = abs(f(x_novo))
        erros.append(erro)

        if erro < tol:
            x = x_novo
            break

        x = x_novo

    return x, i+1, time.time()-inicio, erros


# ==========================================================
# SECANTE
# ==========================================================

def secante(f, x0, x1, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    if tipo == "float32":
        x0, x1 = np.float32(x0), np.float32(x1)

    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)

        if (f1 - f0) == 0:
            break

        if tipo == "float32":
            x2 = np.float32(x1 - f1*(x1-x0)/(f1-f0))
        elif tipo == "trunc":
            x2 = trunc4(x1 - f1*(x1-x0)/(f1-f0))
        else:
            x2 = x1 - f1*(x1-x0)/(f1-f0)

        erro = abs(f(x2))
        erros.append(erro)

        if erro < tol:
            x1 = x2
            break

        x0, x1 = x1, x2

    return x1, i+1, time.time()-inicio, erros


# ==========================================================
# PONTO FIXO
# ==========================================================

def ponto_fixo(g, x0, tol=1e-6, max_iter=100, tipo="float64"):
    erros = []
    inicio = time.time()

    x = np.float32(x0) if tipo=="float32" else x0

    for i in range(max_iter):

        if tipo == "float32":
            x_novo = np.float32(g(x))
        elif tipo == "trunc":
            x_novo = trunc4(g(x))
        else:
            x_novo = g(x)

        erro = abs(f(x_novo))
        erros.append(erro)

        if erro < tol:
            x = x_novo
            break

        x = x_novo

    return x, i+1, time.time()-inicio, erros


# ==========================================================
# EXECUÇÃO
# ==========================================================

a, b = 0, 1
x0 = 0.5

metodos = {
    "Bissecção": lambda tipo: bisseccao(f,a,b,tipo=tipo),
    "Falsa Posição": lambda tipo: falsa_posicao(f,a,b,tipo=tipo),
    "Illinois": lambda tipo: illinois(f,a,b,tipo=tipo),
    "Newton": lambda tipo: newton(f,df,x0,tipo=tipo),
    "Secante": lambda tipo: secante(f,a,b,tipo=tipo),
    "Ponto Fixo": lambda tipo: ponto_fixo(g,x0,tipo=tipo)
}

tipos = ["float64","float32","trunc"]

resultados = {}

for nome, metodo in metodos.items():
    resultados[nome] = {}
    print(f"\n===== {nome} =====")
    for tipo in tipos:
        raiz, it, tempo, erros = metodo(tipo)
        resultados[nome][tipo] = erros
        print(f"{tipo} → raiz: {raiz} | it: {it} | erro final: {erros[-1]}")


# ==========================================================
# GRÁFICOS DE COMPARAÇÃO
# ==========================================================

for nome in resultados:

    plt.figure()

    plt.plot(resultados[nome]["float64"], label="Float64")
    plt.plot(resultados[nome]["float32"], label="Float32")
    plt.plot(resultados[nome]["trunc"], label="Truncamento")

    plt.yscale("log")
    plt.xlabel("Iterações")
    plt.ylabel("Erro |f(x)|")
    plt.title(f"Convergência - {nome}")
    plt.legend()
    plt.grid()

    plt.show()
