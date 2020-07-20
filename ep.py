import sys  # modules
import time
import random
import matplotlib.pyplot as plt

class Grafo(object):
    def iniciar(grafo):
                for v in range(grafo.vertices + 1):
                    grafo.adj.append([])

    def __init__(grafo, path = '', vertice = 1):
        grafo.adj = []

        if path == '':
            grafo.vertices = vertice
            grafo.aresta = 0
            grafo.iniciar()

        else:
            with open(path, 'r') as arquivo:
                grafo.vertices = int(arquivo.readline().rstrip('\n'))
                grafo.aresta = int(arquivo.readline().rstrip('\n'))
                grafo.iniciar()

                for k in range(grafo.aresta):
                    linha = arquivo.readline().rstrip('\n')
                    a, b = linha.split()
                    grafo.adAresta(int(a), int(b))

    def obterVertice(grafo):
        return grafo.vertices

    def obterAresta(grafo):
        return grafo.aresta

    def adAresta(grafo, v, w): # adicionar aresta
        grafo.adj[v].append(w)
        grafo.adj[w].append(v)

    def obterAdj(grafo, v):
        return grafo.adj[v]

    def grau(grafo):
        return len(grafo.adj[v])

    def obterMaiorGrau(grafo):
        obterMaiorGrau = 0
        for i in range(grafo.adj[v]):
            if grafo.adj[v].grau(i) > obterMaiorGrau:
                obterMaiorGrau = grafo.adj[v].grau(i)
        return obterMaiorGrau



class Interacao(object):
    def __init__(inter, grafo, c, r):
        inter.estado = [] # estado da pessoa
        inter.passos = []
        inter.r = r  # para recuperar
        inter.c = c  # para contaminar

        for i in range(grafo.obterVertice()): # Começa com cada vértice marcado como suscetível(S)
            inter.estado.append("S")

        # Exceto um escolhido aleatoriamente que é marcado como infectado (I), este
        # será o paciente zero
        vertice_pacienteInfectado = 0
        inter.estado[vertice_pacienteInfectado] = "I"
        
        quant = { 'S': grafo.obterVertice() - 1, 'I': 1, 'R': 0 }      
        inter.passos.append(quant.copy())

        contador = 0

        while quant['I'] != 0:
            if inter.estado[vertice_pacienteInfectado] != "I":
                
                for i in range(len(inter.estado)):
                    if inter.estado[i] == "I":
                        vertice_pacienteInfectado = i
                        break
            
            quant = inter.dinamica(grafo, vertice_pacienteInfectado, quant)
            contador += 1
        print(f"\n {contador} vezes para I")


    def dinamica(inter, grafo, v, quant):        
        if inter.estado[v] == "I":
            recuperar = random.uniform(0, 1)
            #recuperar = random.random()  # sorteia número - returns a random float number between 0 and 1

            if recuperar < inter.r:  # se x <= r a pessoa se recuperou, então marque v com R
                inter.estado[v] = "R"
                #print(f'{v} recuperado')
                quant['I'] -= 1
                quant['R'] += 1
            else:
                for w in grafo.obterAdj(v):
                    if inter.estado[w] == "S":
                        contaminar = random.uniform(0, 1)
                        #print(f'{w} contaminado')
                        if contaminar <= inter.c:
                            inter.estado[w] = "I"
                            quant['I'] += 1
                            quant['S'] -= 1
                            quant = inter.dinamica(grafo, w, quant)
        
        inter.passos.append(quant.copy())
        return quant

    def obterPassos(inter):
        return inter.passos

    def obterEstado(inter):
        return inter.estado

def modelo(c, r):
    total = c + r
    print(f"Contágio = {c}, Recuperação = {r}, Total = {total}")
    interacao = Interacao(grafo, c, r)
    estado = interacao.obterEstado()
    passos = interacao.obterPassos()
    contarNumPassos = len(passos)

    contador = 0
    for p in passos:        
        contador += 1
        if contador > 10:
            break

    labels = [i+1 for i in range(contarNumPassos)]
    
    infectado = []
    recuperado = []
    
    for i in range(contarNumPassos):
        infectado.append(passos[i]['I'])
        recuperado.append(passos[i]['R'])

    # print(infectado)
    # print(recuperado)

    width = 0.9  # the width of the bars: can also be len(x) sequence
    #width = 0.75
    fig, ax = plt.subplots()

    # gráfico de barras empilhadas 
    # com o número de infectados embaixo e o 
    # de recuperados em cima.
    ax.bar(labels, infectado, width, color='crimson', label='pessoas infectadas')
    ax.bar(labels, recuperado, width, color='cyan', bottom=infectado, label='pessoas recuperadas')
    ax.set_xlabel('Tempo (Número de Passos)')
    ax.set_ylabel('Número de Pessoas')
    plt.grid(axis = 'y', alpha = 0.5)
    plt.grid(axis = 'x', alpha = 0.5)
    # ax.set_title()
    ax.legend()
    #plt.show()


if __name__ == "__main__":
    inicio = time.time()
    sys.setrecursionlimit(2500)
    grafo = Grafo('traducao3.txt')
    #c = 0.7 # coverage da probabilidade fixado entre valores
    #r = 0.1
    c = random.uniform(0, 1) # Return a random floating point number N such that a <= N <= b 
    #c = random.random() # generates a random float uniformly in the semi-open range [0.0, 1.0)
    r = (1 - c) # quando tiver somente recuperados e contaminados

    modelo(c, r)
    
    fim = time.time()
    print("\nTempo de execução: {:.2f} segundos".format(fim-inicio))
    plt.show()