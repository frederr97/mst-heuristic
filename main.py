#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import os

INF = 9999999
custoTotalAGM = INF
def initialize():
    # Leitura e exibição do diretório de entrada
    caminhos = [os.path.join("entrada/", nome) for nome in os.listdir("entrada/")]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    for i in range(len(arquivos)):
        print i, " - ", arquivos[i]
    opcao = raw_input("\nInsira o número equivalente à opção do arquivo que deseja determinar como entrada: ")
    # Inicia a leitura do grafo
    grafo = nx.Graph()
    arq = open(arquivos[int(opcao)])
    linha = arq.readline()
    vertices, arestas = linha.split()            # Recebe a quantidade de vértices e arestas
    linha = arq.readline()                      # Primeira flag -1
    cont = 0
    # Recebendo a posição e peso dos vértices
    for linha in arq:
        if len(linha.split()) < 3:
            break
        else:
            grafo.add_node(cont)
            pos_x, pos_y, peso = linha.split()
            grafo.node[cont]['x'] = int(pos_x)
            grafo.node[cont]['y'] = int(pos_y)
            grafo.node[cont]['weight'] = int(peso)
            cont += 1
    # Recebendo as arestas e seus pesos
    for linha in arq:
        v1, v2, peso = linha.split()
        grafo.add_edge(int(v1), int(v2), weight = int(peso))
        grafo[int(v1)][int(v2)]['added'] = False

    arq.close()

    return grafo


def prim(grafo_residual, grafo):
    arvore = nx.Graph()
    arvore.add_node(0)
    v_add = [0]
    arestas_arvore = []
    custo = 0
    menor_aresta = []
    # Loop para construir a AGM
    while arvore.number_of_nodes() != grafo_residual.number_of_nodes():
        menor_custo = INF
        for vertice in v_add:
            vizinhos = list(grafo_residual.neighbors(vertice))
            for neighbor in range(grafo_residual.degree(vertice)):
                if grafo_residual[vertice][vizinhos[neighbor]]['weight'] < menor_custo:
                    menor_custo = grafo_residual[vertice][vizinhos[neighbor]]['weight']
                    menor_aresta = ([vertice, vizinhos[neighbor]])
        arestas_arvore.append([menor_aresta[0], menor_aresta[1]])
        v_add.append(menor_aresta[1])
        grafo_residual.remove_edge(menor_aresta[0], menor_aresta[1])
        grafo[menor_aresta[0]][menor_aresta[1]]['added'] = True
        custo += menor_custo
        arvore.add_node(menor_aresta[1], weight=grafo_residual.node[menor_aresta[1]]['weight'])

    # Cria a AGM com a lista de arestas obtidas
    
    for i in range(len(arestas_arvore)):
        arvore.add_edge(arestas_arvore[i][0], arestas_arvore[i][1])
    
    print "\nO custo da AGM gerada pelo algoritmo de Prim é %d.\n" % custo
    
    return custo, arestas_arvore, arvore, grafo
'''
def sum_of_costs_AGM(custo_parcial,custoAGM):
    custo_parcial_Total = custo_parcial+ custoAGM
    return custo_parcial

def refinement(custo_parcial_Total,custoTotalAGM):
    if custo_parcial_Total < custoTotalAGM:
        custoTotalAGM = custo_parcial_Total
        return True
    else :
        return False
'''


def calculates_cost(arvore):
    custo_parcial = 0;
    # Soma o custo das arestas da AGM com o custo dos vértices
    for vertice in arvore.nodes():
        for neighbor in range(arvore.degree(vertice)):
            custo_parcial += arvore[vertice][neighbor]
        if arvore.degree(vertice) > 1:
            custo_parcial += arvore.node[vertice]['weight']

    return custo_parcial            


def refinement_heuristic(grafo, arvore, custo):
    # Função que remolda a AGM de acordo com o a heurística
    for aresta in range(grafo.number_of_edges()):
        if grafo[aresta]["added"] == False:
            arvore.add_edges([(grafo.es[aresta].source, grafo.es[aresta].target)])



def main():
    os.system('cls')
    grafo = initialize()
    grafo_residual = grafo.copy()
    custo, arestas_arvore, arvore, grafo = prim(grafo_residual, grafo)
    custo_parcial = calculates_cost(arvore)
    custoTotal= sum_of_costs_AGM(custo, custo_parcial)
    boolean =  refinement(custoTotal, custoTotalAGM)
    print boolean
    #refinement_heuristic(grafo, arvore, custo)

if __name__ == '__main__':
      main()  