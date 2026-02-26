import numpy as np
import matplotlib.pyplot as plt
import time

# FUNÇÕES E DERIVADAS
def f1(x):
    return x**3 - 7*x + 6

def df1(x):
    return 3*x**2 - 7

# g1(x) para Ponto Fixo de f1: isolando x → x = (x³ + 6) / 7
def g1(x):
    return (x**3 + 6) / 7

def f2(x):
    return np.log(x + 1) + x - 2

def df2(x):
    return 1/(x + 1) + 1

# g2(x) para ponto fixo de f2: isolando x → x = 2 - ln(x + 1)
def g2(x):
    return 2 - np.log(x + 1)

# MÉTODOS
def bisseccao(f, inicio, fim, tol=1e-6, max_iter=100):
    lista = []
    t_inicio = time.perf_counter()
    for i in range(max_iter):
        meio = (inicio + fim) / 2
        lista.append(meio)
        if abs(f(meio)) < tol:
            break
        if f(inicio) * f(meio) < 0:
            fim = meio
        else:
            inicio = meio
    tempo = time.perf_counter() - t_inicio
    return meio, lista, tempo

def falsa_posicao(f, inicio, fim, tol=1e-6, max_iter=100):
    lista = []
    t_inicio = time.perf_counter()
    for i in range(max_iter):
        falso = (inicio * f(fim) - fim * f(inicio)) / (f(fim) - f(inicio))
        lista.append(falso)
        if abs(f(falso)) < tol:
            break
        if f(inicio) * f(falso) < 0:
            fim = falso
        else:
            inicio = falso
    tempo = time.perf_counter() - t_inicio
    return falso, lista, tempo

def newton(f, df, chute, tol=1e-6, max_iter=100):
    lista = []
    inicio = time.perf_counter()
    for i in range(max_iter):
        proximo = chute - f(chute) / df(chute)
        lista.append(proximo)
        if abs(f(proximo)) < tol:
            break
        chute = proximo
    tempo = time.perf_counter() - inicio
    return proximo, lista, tempo

def secante(f, chute1, chute2, tol=1e-6, max_iter=100):
    lista = []
    inicio = time.perf_counter()
    for i in range(max_iter):
        proximo = chute2 - f(chute2)*(chute2 - chute1) / (f(chute2) - f(chute1))
        lista.append(proximo)
        if abs(f(proximo)) < tol:
            break
        chute1, chute2 = chute2, proximo
    tempo = time.perf_counter() - inicio
    return proximo, lista, tempo

def ponto_fixo(f, g, chute, tol=1e-6, max_iter=100):
    lista = []
    inicio = time.perf_counter()
    for i in range(max_iter):
        proximo = g(chute)
        lista.append(proximo)
        if abs(proximo - chute) < tol:
            break
        chute = proximo
    tempo = time.perf_counter() - inicio
    return proximo, lista, tempo

# DIAGNÓSTICO
def diagnostico(nome, f, raiz, lista, tempo, tol=1e-6):
    convergiu = abs(f(raiz)) < tol and not (raiz != raiz or raiz == float('inf') or raiz == float('-inf'))
    status = "CONVERGENTE ✓" if convergiu else "DIVERGENTE ✗"

    if len(lista) >= 2:
        erro_arred_abs = abs(lista[-1] - lista[-2])
    else:
        erro_arred_abs = float('nan')

    if abs(raiz) > 0:
        erro_arred_rel = erro_arred_abs / abs(raiz)
    else:
        erro_arred_rel = float('nan')

    erro_trunc = abs(f(raiz))

    print("  " + "─"*38)
    print("  " + nome + ": " + status)
    print("  Iterações                    : " + str(len(lista)))
    print("  Erro Arredondamento Absoluto : " + str(round(erro_arred_abs, 10)))
    print("  Erro Arredondamento Relativo : " + str(round(erro_arred_rel, 10)))
    print("  Erro de Truncamento          : " + str(round(erro_trunc, 10)))
    print("  Raiz encontrada              : " + str(round(raiz, 8)))

    return status, len(lista), tempo, convergiu

# EXECUÇÃO: FUNÇÃO 1
print("=" * 42)
print("  FUNÇÃO 1: f(x) = x³ - 7x + 6")
print("=" * 42)

raiz_new1, lista_new1, tempo_new1 = newton(f1, df1, chute=0.5)
raiz_sec1, lista_sec1, tempo_sec1 = secante(f1, chute1=0.5, chute2=1.5)
raiz_pf1,  lista_pf1,  tempo_pf1  = ponto_fixo(f1, g1, chute=0.5)
raiz_bis1, lista_bis1, tempo_bis1 = bisseccao(f1, inicio=-4, fim=0)
raiz_fp1,  lista_fp1,  tempo_fp1  = falsa_posicao(f1, inicio=-4, fim=0)

status_new1, iter_new1, t_new1, conv_new1 = diagnostico("Newton",        f1, raiz_new1, lista_new1, tempo_new1)
status_sec1, iter_sec1, t_sec1, conv_sec1 = diagnostico("Secante",       f1, raiz_sec1, lista_sec1, tempo_sec1)
status_pf1,  iter_pf1,  t_pf1,  conv_pf1  = diagnostico("Ponto Fixo",   f1, raiz_pf1,  lista_pf1,  tempo_pf1)
status_bis1, iter_bis1, t_bis1, conv_bis1 = diagnostico("Bissecção",     f1, raiz_bis1, lista_bis1, tempo_bis1)
status_fp1,  iter_fp1,  t_fp1,  conv_fp1  = diagnostico("Falsa Posição", f1, raiz_fp1,  lista_fp1,  tempo_fp1)

# EXECUÇÃO: FUNÇÃO 2
print("=" * 42)
print("  FUNÇÃO 2: f(x) = ln(x+1) + x - 2")
print("=" * 42)

raiz_new2, lista_new2, tempo_new2 = newton(f2, df2, chute=1.0)
raiz_sec2, lista_sec2, tempo_sec2 = secante(f2, chute1=1.0, chute2=2.0)
raiz_pf2,  lista_pf2,  tempo_pf2  = ponto_fixo(f2, g2, chute=1.0)
raiz_bis2, lista_bis2, tempo_bis2 = bisseccao(f2, inicio=0.5, fim=2.0)
raiz_fp2,  lista_fp2,  tempo_fp2  = falsa_posicao(f2, inicio=0.5, fim=2.0)

status_new2, iter_new2, t_new2, conv_new2 = diagnostico("Newton",        f2, raiz_new2, lista_new2, tempo_new2)
status_sec2, iter_sec2, t_sec2, conv_sec2 = diagnostico("Secante",       f2, raiz_sec2, lista_sec2, tempo_sec2)
status_pf2,  iter_pf2,  t_pf2,  conv_pf2  = diagnostico("Ponto Fixo",   f2, raiz_pf2,  lista_pf2,  tempo_pf2)
status_bis2, iter_bis2, t_bis2, conv_bis2 = diagnostico("Bissecção",     f2, raiz_bis2, lista_bis2, tempo_bis2)
status_fp2,  iter_fp2,  t_fp2,  conv_fp2  = diagnostico("Falsa Posição", f2, raiz_fp2,  lista_fp2,  tempo_fp2)

# RANKING
def imprimir_ranking(titulo, nomes, iteracoes, convergencias):
    print("  " + titulo)
    print("  " + "─"*40)
    print("  #    Método                Iterações")
    print("  " + "─"*40)

    # Separa convergentes e divergentes
    conv_nomes = []
    conv_iters = []
    div_nomes  = []

    for i in range(len(nomes)):
        if convergencias[i]:
            conv_nomes.append(nomes[i])
            conv_iters.append(iteracoes[i])
        else:
            div_nomes.append(nomes[i])

    # Ordena do menor para o maior número de iterações
    for i in range(len(conv_iters)):
        for j in range(i + 1, len(conv_iters)):
            if conv_iters[j] < conv_iters[i]:
                conv_iters[i], conv_iters[j] = conv_iters[j], conv_iters[i]
                conv_nomes[i], conv_nomes[j] = conv_nomes[j], conv_nomes[i]

    posicao = 1
    for i in range(len(conv_nomes)):
        linha = "  " + str(posicao) + "    " + conv_nomes[i].ljust(22) + str(conv_iters[i])
        print(linha)
        posicao = posicao + 1

    if len(div_nomes) > 0:
        print("  " + "─"*40)
        print("  Divergentes:")
        for nome in div_nomes:
            print("  ✗  " + nome)

print("")
print("=" * 42)
print("  RANKING DE EFICIÊNCIA")
print("=" * 42)

# Todos os resultados e identificação da função
todos_nomes = [
    "Newton        F1", "Secante       F1", "Ponto Fixo    F1", "Bissecção     F1", "Falsa Posição F1",
    "Newton        F2", "Secante       F2", "Ponto Fixo    F2", "Bissecção     F2", "Falsa Posição F2",
]
todos_iters = [iter_new1, iter_sec1, iter_pf1, iter_bis1, iter_fp1,
               iter_new2, iter_sec2, iter_pf2, iter_bis2, iter_fp2]
todos_tempos = [t_new1, t_sec1, t_pf1, t_bis1, t_fp1,
                t_new2, t_sec2, t_pf2, t_bis2, t_fp2]
todos_convs  = [conv_new1, conv_sec1, conv_pf1, conv_bis1, conv_fp1,
                conv_new2, conv_sec2, conv_pf2, conv_bis2, conv_fp2]
conv_nomes  = []
conv_iters  = []
conv_tempos = []
div_nomes   = []
for i in range(len(todos_nomes)):
    if todos_convs[i]:
        conv_nomes.append(todos_nomes[i])
        conv_iters.append(todos_iters[i])
        conv_tempos.append(todos_tempos[i])
    else:
        div_nomes.append(todos_nomes[i])
# Ordenação por comparação
for i in range(len(conv_iters)):
    for j in range(i + 1, len(conv_iters)):
        if conv_iters[j] < conv_iters[i]:
            conv_iters[i],  conv_iters[j]  = conv_iters[j],  conv_iters[i]
            conv_tempos[i], conv_tempos[j] = conv_tempos[j], conv_tempos[i]
            conv_nomes[i],  conv_nomes[j]  = conv_nomes[j],  conv_nomes[i]
print("")
print("  " + "─"*52)
print("  #    Método                 Iterações   Tempo (µs)")
print("  " + "─"*52)
posicao = 1
for i in range(len(conv_nomes)):
    tempo_us = round(conv_tempos[i] * 1e6, 2) #arredonda e escolhe max de casas decimais
    print("  " + str(posicao) + "    " + conv_nomes[i].ljust(23) + str(conv_iters[i]).ljust(12) + str(tempo_us))
    posicao = posicao + 1
if len(div_nomes) > 0:
    print("  " + "─"*52)
    print("  Divergentes:")
    for nome in div_nomes:
        print("  ✗  " + nome)

# GRÁFICOS
# Função 1
plt.plot(lista_new1)
plt.title("F1 — Newton\n" + status_new1)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_sec1)
plt.title("F1 — Secante\n" + status_sec1)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_pf1)
plt.title("F1 — Ponto Fixo\n" + status_pf1)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_bis1)
plt.title("F1 — Bissecção\n" + status_bis1)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_fp1)
plt.title("F1 — Falsa Posição\n" + status_fp1)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

# Função 2
plt.plot(lista_new2)
plt.title("F2 — Newton\n" + status_new2)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_sec2)
plt.title("F2 — Secante\n" + status_sec2)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_pf2)
plt.title("F2 — Ponto Fixo\n" + status_pf2)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_bis2)
plt.title("F2 — Bissecção\n" + status_bis2)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()

plt.plot(lista_fp2)
plt.title("F2 — Falsa Posição\n" + status_fp2)
plt.xlabel("Iteração")
plt.ylabel("Aproximação")
plt.show()