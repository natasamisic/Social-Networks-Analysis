# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 18:36:14 2022

@author: Natasa
"""
import networkx as nx
import random 
import matplotlib.pyplot as plt

def ucitaj_rucni_klasterabilan_graf():
    graf = nx.Graph()
    
    for i in range(1, 19):
        graf.add_node(i)
        
    graf.add_edge(1, 2, label="-")
    graf.add_edge(1, 3, label="-")     
    
    graf.add_edge(2, 4, label="+")
    graf.add_edge(3, 4, label="+")
    graf.add_edge(4, 6, label="+")
    graf.add_edge(4, 5, label="+")
    
    graf.add_edge(4, 7, label="-")
    graf.add_edge(5, 11, label="-")
    graf.add_edge(7, 8, label="-")
    graf.add_edge(8, 9, label="+")
    graf.add_edge(9, 10, label="-")
    
    graf.add_edge(10, 11, label="-")
    graf.add_edge(11, 12, label="-")
    graf.add_edge(11, 15, label="-")
    
    graf.add_edge(12, 13, label="-")
    graf.add_edge(12, 14, label="+")
    graf.add_edge(15, 16, label="-")
    graf.add_edge(16, 17, label="+")

    graf.add_edge(17, 18, label="+")
    graf.add_edge(18, 16, label="+")
    
    prikazi_graf(graf, "Rucno napravljen klasterabilan graf")
    return graf;

def ucitaj_rucni_neklasterabilan_graf():
    graf = nx.Graph()
    
    for i in range(1, 21):
        graf.add_node(i)
        
    graf.add_edge(1, 2, label="-")
    graf.add_edge(1, 3, label="-")     
    
    graf.add_edge(2, 4, label="+")
    graf.add_edge(3, 4, label="+")
    graf.add_edge(4, 6, label="+")
    graf.add_edge(4, 5, label="+")
    
    graf.add_edge(4, 7, label="-")
    graf.add_edge(5, 11, label="-")
    graf.add_edge(5, 7, label="+")
    graf.add_edge(7, 8, label="-")
    graf.add_edge(8, 9, label="+")
    graf.add_edge(9, 10, label="-")
    
    graf.add_edge(10, 11, label="-")
    graf.add_edge(11, 12, label="-")
    graf.add_edge(11, 15, label="-")
    
    graf.add_edge(12, 13, label="-")
    graf.add_edge(12, 14, label="+")
    graf.add_edge(15, 16, label="-")
    graf.add_edge(16, 17, label="+")

    graf.add_edge(17, 18, label="+")
    graf.add_edge(18, 16, label="+")
    graf.add_edge(13, 20, label="+")
    graf.add_edge(19, 14, label="-")
    graf.add_edge(19, 20, label="+")
    graf.add_edge(20, 14, label="+")
    
    prikazi_graf(graf, "Rucno napravljen neklasterabilan graf")
    return graf;

def ucitaj_random_graf():
    graf = nx.Graph()
    broj_cvorova = random.randrange(70, 200)
    broj_klastera = random.randrange(2, round(broj_cvorova/2))
    
    for i in range(1, broj_cvorova):
        graf.add_node(i)
        
    klasteri = []
    i = 0
    while i <= broj_klastera:
        kl = nx.Graph()
        cvor = list(graf.nodes)[i]
        kl.add_node(cvor)
        klasteri.append(kl)
        i += 1
        
    for c in list(graf.nodes)[broj_klastera+1:]:
        k = random.randrange(1, broj_klastera)
        klasteri[k].add_node(c)
        
    vrv = 0.46
    for k in klasteri:
        for cvor in k.nodes:
            random_cvor = random.randint(1, len(k.nodes))
            if cvor != list(k.nodes)[random_cvor-1]:
                if random.uniform(0, 1) < vrv:    
                    graf.add_edge(cvor, list(k.nodes)[random_cvor-1], label = "+")
                elif random.uniform(0, 1) < vrv:
                    graf.add_edge(cvor, list(k.nodes)[random_cvor-1], label = "-")
        for k1 in klasteri:
            if k == k1: 
                continue
            if random.uniform(0, 1) < vrv:
                random_cvor1 = random.randint(1, len(k.nodes))
                random_cvor2 = random.randint(1, len(k1.nodes))   
                graf.add_edge(list(k.nodes)[random_cvor1-1], list(k1.nodes)[random_cvor2-1], label = "-")
    
    #prikazi_graf(graf, "Random generisan graf".format(naslov))
    return graf;

def ucitaj_epinions_slashdot_graf(path):
    graf = nx.DiGraph()
    file = open(path, "r")
    lines = file.read().splitlines()
    for line in lines:
        if line.startswith("#"):
            continue
        line = line.split("\t")
        if int(line[2]) > 0:
            znak = "+"
        else:
            znak = "-"
        graf.add_edge(line[0].strip(), line[1].strip(), label = znak)
    return prebaci_u_neusmeren_graf(graf);

def ucitaj_wiki_graf(path):
    graf = nx.DiGraph()
    file = open(path, "r", encoding="utf8")
    lines = file.read().splitlines()
    for line in lines:
        if line.startswith("SRC"):
            cvorA = line.split(":")[1]
            if cvorA not in graf.nodes:
                graf.add_node(cvorA)
        if line.startswith("TGT"):
            cvorB = line.split(":")[1]
            if cvorB not in graf.nodes:
                graf.add_node(cvorB)
        if line.startswith("VOT"):
            znak = line.split(":")[1]
            if znak == "1":
                znak = "+"
                graf.add_edge(cvorA, cvorB, label = znak)
            elif znak == "-1":
                znak = "-"
                graf.add_edge(cvorA, cvorB, label = znak)
    return prebaci_u_neusmeren_graf(graf);

def prebaci_u_neusmeren_graf(usmeren_graf):
    graf = nx.Graph()
    graf.add_nodes_from(usmeren_graf.nodes())
    graf.add_edges_from(usmeren_graf.edges(), label="")
    for u, v, d in usmeren_graf.edges(data=True):
        znak1 = usmeren_graf[u][v]['label']
        znak2 = ""
        if (v, u) in usmeren_graf.edges:
            znak2 = usmeren_graf[v][u]['label']
        if znak1 == "-" or znak2 == "-":
            graf[u][v]['label'] = "-"
        else:
            graf[u][v]['label'] = "+"
    return graf;

def prikazi_graf(graf, naslov):
    layout = nx.kamada_kawai_layout(graf)
    nx.draw_networkx_labels(graf, layout)
    nx.draw_networkx_nodes(graf.nodes, pos = layout)
    e_plus = [(u, v) for (u, v, d) in graf.edges(data=True) if d['label'] == "+"]
    e_minus = [(u, v) for (u, v, d) in graf.edges(data=True) if d['label'] == "-"]
    nx.draw_networkx_edges(graf, layout, edgelist = e_plus, width=2.0, edge_color='blue')
    nx.draw_networkx_edges(graf, layout, edgelist = e_minus, width=2.0, edge_color= 'blue', style='dashed')
    plt.title(naslov)
    plt.show();
    
def prikazi_mrezu_klastera(graf, naslov):
    layout = nx.kamada_kawai_layout(graf)
    nx.draw_networkx_labels(graf , layout)
    nx.draw_networkx_nodes(graf.nodes, pos = layout)
    nx.draw_networkx_edges(graf, layout, width=2.0, edge_color= 'blue', style='dashed')
    plt.title(naslov)
    plt.show() 
        