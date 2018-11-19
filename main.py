#!/usr/bin/env python
# -*- coding: utf-8 -*-

from igraph import *


def initialize():
	grafo = Graph()
	arq = open('entrada/v100_d30_t1_i1.dat')
	linha = arq.readline()
	vertices, arestas = linha.split()		# Receive vertices and arestas
	grafo.add_vertices(int(vertices))
	linha = arq.readline()				# First -1 flag
	cont = 0
	# Receiving the position and weight of vertices
	for linha in arq:
		if len(linha.split()) < 3:
			break	
		else:
			pos_x, pos_y, peso = linha.split()
			grafo.vs[cont]["x"] = int(pos_x)
			grafo.vs[cont]["y"] = int(pos_y)
			grafo.vs[cont]["weight"] = int(peso)
			cont += 1
	# Receiving the edges and respective weights
	for linha in arq:
		v1, v2, peso = linha.split()
		grafo.add_edges([(int(v1),int(v2))])
		grafo.es[grafo.get_eid(int(v1),int(v2))]["weight"] = int(peso)  

	arq.close()
	return grafo

def prim(grafo):
	# Setting the "added" flag of all vertices and edges to False
	for vertice in grafo.vs:
		grafo.vs[vertice]["added"] = False
	arvore = Graph()
	arvore.add_vertex()
	print arvore
	v_add = [0]
	arestas_arvore = []
	# Loop to construct the minimum spanning tree			 
	while arvore.gvcount() != grafo.gvcount():
		aresta_peso = []
		for vertice in v_add:
			for aresta in grafo.incident(vertice):
				aresta_peso.append([aresta, grafo.es[aresta]["weight"]])
		aresta_peso.sort(key=lambda x: x[1])
		arestas_arvore.append([aresta_peso[0][0].source, aresta_peso[0][0].target])
		v_add.append(grafo.es[aresta_peso[0][0]].target)
		grafo.delete_edges(aresta_peso[0][0])
		custo += aresta_peso[0][1]
		arvore.add_vertex()
	# Create the MST with edges list obtained
	for i in len(arestas_arvore):
		arvore.add_edges([(arestas_arvore[i][0], arestas_arvore[i][1])])
		print arestas_arvore[i]
		

def main():
	grafo = initialize()
	prim(grafo)

if __name__ == '__main__':
    main()
