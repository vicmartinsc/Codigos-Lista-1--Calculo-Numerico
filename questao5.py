import numpy as np
import matplotlib.pyplot as plt

T, L, g = 2, 1.0, 9.81

def f(theta):
    return np.sin(theta) - (T / (2 * np.pi)) * np.sqrt(g / L)

def df(theta):
    return np.cos(theta)

def bisseccao(inicio, fim, tol=1e-6, max_iter=100):
    lista = []
    for i in range(max_iter):
        meio = (inicio + fim) / 2
        lista.append(meio)
        if abs(f(meio)) < tol:
            break
        if f(inicio) * f(meio) < 0:
            fim = meio
        else:
            inicio = meio
    return meio, lista

def newton(chute, tol=1e-6, max_iter=100):
    lista = []
    for i in range(max_iter):
        proximo = chute - f(chute) / df(chute)
        lista.append(proximo)
        if abs(f(proximo)) < tol:
            break
        chute = proximo
    return proximo, lista

def secante(chute1, chute2, tol=1e-6, max_iter=100):
    lista = []
    for i in range(max_iter):
        proximo = chute2 - f(chute2) * (chute2 - chute1) / (f(chute2) - f(chute1))
        lista.append(proximo)
        if abs(f(proximo)) < tol:
            break
        chute1, chute2 = chute2, proximo
    return proximo, lista

def falsa_posicao(inicio, fim, tol=1e-6, max_iter=100):
    lista = []
    for i in range(max_iter):
        falso = (inicio * f(fim) - fim * f(inicio)) / (f(fim) - f(inicio))
        lista.append(falso)
        if abs(f(falso)) < tol:
            break
        if f(inicio) * f(falso) < 0:
            fim = falso
        else:
            inicio = falso
    return falso, lista

def ponto_fixo(chute, tol=1e-6, max_iter=100):
    lista = []
    constante = (T / (2 * np.pi)) * np.sqrt(g / L)
    if abs(constante) <= 1:               #arco seno
        for i in range(max_iter):
            proximo = np.arcsin(constante)
            lista.append(proximo)
            if abs(proximo - chute) < tol:
                break
            chute = proximo
    else:
        for i in range(max_iter):         #seno
            proximo = chute - (np.sin(chute) - constante)
            lista.append(proximo)
            if abs(proximo - chute) < tol:
                break
            chute = proximo
    return proximo, lista

# Execução
raiz_bis, lista_bis = bisseccao(0, 2)
raiz_new, lista_new = newton(1)
raiz_sec, lista_sec = secante(0.5, 1.5)
raiz_fp,  lista_fp  = falsa_posicao(0, 2)
raiz_pf,  lista_pf  = ponto_fixo(1)

def diagnostico(nome, raiz, lista, tol=1e-6):
    convergiu = abs(f(raiz)) < tol and not (raiz != raiz or raiz == float('inf') or raiz == float('-inf'))
    status = "CONVERGENTE ✓" if convergiu else "DIVERGENTE ✗"

    # diferença entre as 2 últimas iterações
    if len(lista) >= 2:
        erro_arred_abs = abs(lista[-1] - lista[-2])
    else:
        erro_arred_abs = float('nan') #nan - valor não válido por conta da quantidade de iterações

    # erro absoluto dividido pelo valor atual
    if abs(raiz) > 0:
        erro_arred_rel = erro_arred_abs / abs(raiz)
    else:
        erro_arred_rel = float('nan')

    erro_trunc = abs(f(raiz))

    print(f"\n{'='*40}")
    print(f"  {nome}: {status}")
    print(f"  Iterações                    : {len(lista)}")
    print(f"  Erro Arredondamento Absoluto : {erro_arred_abs:.2e}")
    print(f"  Erro Arredondamento Relativo : {erro_arred_rel:.2e}")
    print(f"  Erro de Truncamento          : {erro_trunc:.2e}")
    print(f"  Raiz encontrada              : {raiz:.8f}")

    return status

# Diagnóstico e coleta de status para os gráficos
status_bis = diagnostico("Bissecção",     raiz_bis, lista_bis)
status_new = diagnostico("Newton",        raiz_new, lista_new)
status_sec = diagnostico("Secante",       raiz_sec, lista_sec)
status_fp  = diagnostico("Falsa Posição", raiz_fp,  lista_fp)
status_pf  = diagnostico("Ponto Fixo",    raiz_pf,  lista_pf)

# Gráficos
metodos = {
    "Bissecção":     (lista_bis, status_bis),
    "Newton":        (lista_new, status_new),
    "Secante":       (lista_sec, status_sec),
    "Falsa Posição": (lista_fp,  status_fp),
    "Ponto Fixo":    (lista_pf,  status_pf),
}

for nome, (lista, status) in metodos.items():
    plt.plot(lista)
    plt.title(f"{nome} — {status}")
    plt.xlabel("Iteração")
    plt.ylabel("Aproximação de θ (radianos)")
    plt.show()