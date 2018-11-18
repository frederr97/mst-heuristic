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

def main():
	initialize()

if __name__ == '__main__':
    main()