# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 20:06:28 2022

@author: Natasa
"""
import networkx as nx

poseceni = []

def pronadji_klastere(graf):
    global poseceni
    komponente = []
    broj_klastera = 0
    for cvor in graf.nodes:
        if cvor not in poseceni:
            komponente.append(bfs(graf, cvor))
            broj_klastera += 1
    return komponente;
        
def bfs(graf, cvor):
    global poseceni
    komp = []
    queue = []
    poseceni.append(cvor)
    queue.append(cvor)
    komp.append(cvor)
    while queue:
        s = queue.pop(0)
        susedi = nx.neighbors(graf, s)
        for sused in susedi:
            e = graf.get_edge_data(s, sused)
            if e['label'] == "-":
                continue
            if sused not in poseceni:
                poseceni.append(sused)
                queue.append(sused)
                komp.append(sused)
    return komp;

def kreiraj_klastere(lista_klastera, grane):
        klasteri = []
        for k in lista_klastera:
            tmp_graf = nx.Graph()
            if len(k) == 1:
                tmp_graf.add_node(k[0])
                klasteri.append(tmp_graf)
                continue
            for g in grane:
                cvor1 = g[0]
                cvor2 = g[1]
                znak = g[2].get('label')
                if cvor1 in k and cvor2 in k:
                    tmp_graf.add_edge(cvor1, cvor2, label=znak)
            klasteri.append(tmp_graf)
        return klasteri;
    
def pronadji_koalicije_i_antikoalicije(klasteri):
    rezultat = []
    koalicije = []
    antikoalicije = []
    linkovi = []
    for k in klasteri:
        losi_linkovi = [(u, v) for (u, v, d) in k.edges(data=True) if d['label'] == "-"]
        if losi_linkovi:
            antikoalicije.append(k)
            for l in losi_linkovi:
                linkovi.append(l)
        else:
            koalicije.append(k)
    rezultat.append(koalicije)
    rezultat.append(antikoalicije)
    rezultat.append(linkovi)
    print(f"\nLosih linkova ima {len(linkovi)}")
    return rezultat;

def konstruisi_mrezu_klastera(graf, klasteri):
    res_graf = nx.Graph()
    i = 1
    for k in klasteri:
        res_graf.add_node(k)
    
    for k1 in klasteri:
        for k2 in klasteri:
            if k1 == k2:
                continue
            povezani = False
            i = 0
            while not povezani and i < len(k1.nodes):
                cvor1 = list(k1.nodes)[i]
                for cvor2 in k2:
                    if cvor1 in nx.neighbors(graf, cvor2):
                        povezani = True
                i += 1
            if povezani:
                res_graf.add_edge(k1, k2)
    nx.set_edge_attributes(res_graf, "-", "label")
    res_graf = nx.convert_node_labels_to_integers(res_graf, first_label=1)
    return res_graf;