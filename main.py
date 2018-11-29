#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import os
import sys


INF = 9999999
parent = dict()
rank = dict()

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
            grafo.node[cont]['pos'] = (int(pos_x), int(pos_y))
            grafo.node[cont]['weight'] = int(peso)
            cont += 1
    # Recebendo as arestas e seus pesos
    for linha in arq:
        v1, v2, peso = linha.split()
        grafo.add_edge(int(v1), int(v2), weight = int(peso))
        grafo[int(v1)][int(v2)]['added'] = False

    arq.close()

    return grafo


def prim(grafo):
    grafo_residual = grafo.copy()
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
        arvore.add_node(menor_aresta[1], weight=grafo_residual.node[menor_aresta[1]]['weight'])

    # Cria a AGM com a lista de arestas obtidas
    
    for i in range(len(arestas_arvore)):
        arvore.add_edge(arestas_arvore[i][0], arestas_arvore[i][1])

    custo = calculates_cost(arvore, grafo)
    print "\nO custo da AGMI gerada pelo algoritmo de Prim é %d.\n" % custo
    
    return custo, arvore, grafo


def calculates_cost(arvore, grafo):
    custo_parcial = 0;
    # Soma o custo dos vértices não-folhas da AGM
    for vertice in arvore.nodes():
        if arvore.degree(vertice) > 1:
            custo_parcial += grafo.node[vertice]['weight']
    # Soma o custo das arestas da AGM ao custo parcial anterior
    for aresta in arvore.edges():
        v1, v2 = aresta
        custo_parcial += grafo[v1][v2]['weight']

    return custo_parcial            


def kruskal(grafo):
    peso=0
    arestas=[]
    for vertice in grafo.nodes():
        make_set(vertice)
        agm = set()
        edges = list(grafo.edges())
        edges.sort()
    arestas=[]
    for edge in edges:
        vertice1, vertice2 = edge
        edge = (grafo[vertice1][vertice2]['weight'],vertice1,vertice2)
        arestas.append(edge)
        arestas.sort()
    for aresta in arestas:
        pesosA,vertice1, vertice2 = aresta
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            agm.add(aresta)
            peso += pesosA
    return peso,sorted(agm)


def return_edges_Kruskal(grafo,mst):
    arvore = nx.Graph()
    new_mst=[]
    for node in grafo.nodes():
        arvore.add_node(node,weight=grafo.node[node]['weight'])
    for i in range(len(mst)):
        arvore.add_edge(mst[i][1], mst[i][2])
        grafo[mst[i][1]][mst[i][2]]['added'] = True
    for element in mst:
        new_mst.append([element[1],element[2]])
    custo = calculates_cost(arvore,grafo)
    print "\nO custo da AGMI gerada pelo algoritmo de Kruskal é %d.\n" % custo
    return arvore,new_mst, custo


def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0


def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]


def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else: 
            parent[root1] = root2
        if rank[root1] == rank[root2]:
            rank[root2] += 1


def refinement_heuristic(grafo, arvore, custo):
    # Função que remolda a AGM de acordo com o a heurística
    for vertice in range(grafo.number_of_nodes()):
        vizinhos = list(grafo.neighbors(vertice))
        for neighbor in range(grafo.degree(vertice)):
            if (vertice != vizinhos[neighbor]) and (grafo.has_edge(vizinhos[neighbor], vertice)):
                if grafo[vertice][vizinhos[neighbor]]['added'] == False:
                    arvore.add_edge(vertice, vizinhos[neighbor])
                # Verifica se a árvore possui ciclo com a nova aresta inserida
                aux = nx.cycle_basis(arvore)
                ciclo = [zip(nodes,(nodes[1:]+nodes[:1])) for nodes in aux]      
                nova_aresta = None            
                if len(ciclo) > 0:
                    for aresta in ciclo[0]:  
                        if aresta != (vertice, vizinhos[neighbor]) or aresta != (vizinhos[neighbor], vertice):                   # Compara se a aresta em questão é a mesma que foi inserida
                            arvore.remove_edge(aresta[0], aresta[1])
                            custo_parcial = calculates_cost(arvore, grafo)
                            if custo_parcial < custo:
                                custo = custo_parcial                       # Altera o custo se a AGM encontrada possuir menor custo
                                nova_aresta = aresta
                                arvore.add_edge(aresta[0], aresta[1])
                            else:
                                arvore.add_edge(aresta[0], aresta[1])       # Devolve a aresta inserida, caso o custo encontrado for maior que o atual
                
                if nova_aresta != None:
                    arvore.remove_edge(nova_aresta[0], nova_aresta[1])
                    grafo[vertice][vizinhos[neighbor]]['added'] = True
                    grafo[nova_aresta[0]][nova_aresta[1]]['added'] = False
                elif grafo[vertice][vizinhos[neighbor]]['added'] == False:
                    arvore.remove_edge(vertice, vizinhos[neighbor])

    print "O custo da nova AGMI gerada pela heurística de refinamento é %d.\n" % custo

    return arvore, custo


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    grafo = initialize()
    os.system('cls' if os.name == 'nt' else 'clear')
    opcao = INF
    pos = nx.get_node_attributes(grafo, 'pos')
    while opcao < 0 or opcao > 2:
        opcao = int(raw_input("1 - Prim\n2 - Kruskal(Union and Find)\n0 - Sair\n\nInsira o número equivalente à opção do algoritmo que deseja executar como solução inicial: "))
        if opcao == 1:
            custo, arvore, grafo = prim(grafo)    
        elif opcao == 2:
            custo, mst = kruskal(grafo)
            arvore, mst, custo = return_edges_Kruskal(grafo, mst)
            nx.draw(arvore, pos, with_labels=True)
            plt.show()
        elif opcao == 0:
            sys.exit()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print "\nVocê digitou uma opção inválida. Tente novamente.\n"  
    
    arvore, custo = refinement_heuristic(grafo, arvore, custo)
    nx.draw(arvore, pos, with_labels=True)
    plt.show()

if __name__ == '__main__':
      main()