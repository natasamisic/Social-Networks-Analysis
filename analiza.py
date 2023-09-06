# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 18:58:24 2022

@author: Natasa
"""
import networkx as nx

def analiza_koalicija_i_antikoalicija(koalicije, antikoalicije):
    metrike_koalicije = metrike(koalicije)
    antikoalicije_postoje = False
    if len(antikoalicije) > 0:
        metrike_antikoalicije = metrike(antikoalicije)
        antikoalicije_postoje = True
    
    print(f"=>Prosecan dijametar klastera koalicije iznosi {metrike_koalicije['dijametar']}")
    if antikoalicije_postoje: 
        print(f"=>Prosecan dijametar klastera antikoalicije iznosi {metrike_antikoalicije['dijametar']}")
    
    print(f"\n=>Prosecna vrednost svih prosecnih stepeni klastera koalicije iznosi {metrike_koalicije['prosecan_stepen']}")
    if antikoalicije_postoje:
        print(f"=>Prosecna vrednost svih prosecnih stepeni klastera antikoalicije iznosi {metrike_antikoalicije['prosecan_stepen']}")
    
    print(f"\n=>Prosecna distanca cvorova koalicije iznosi {metrike_koalicije['prosecna_distanca']}")
    if antikoalicije_postoje:
        print(f"=>Prosecna distanca cvorova antikoalicije iznosi {metrike_antikoalicije['prosecna_distanca']}")
    
    
    
def metrike(klasteri):
    rezultati = {'dijametar': [], 'prosecan_stepen': [], 'prosecna_distanca': []}
    for k in klasteri:
        tmp = nx.diameter(k)
        rezultati['dijametar'].append(tmp)
        
        tmp = prosecan_stepen(k)
        rezultati['prosecan_stepen'].append(tmp)
        
        tmp = nx.average_shortest_path_length(k)
        rezultati['prosecna_distanca'].append(tmp)
    return prosecne_vrednosti(rezultati);

def prosecan_stepen(klaster):
    return sum([d for (n, d) in nx.degree(klaster)]) / float(klaster.number_of_nodes());

def prosecne_vrednosti(rezultati):
    prosek_rez = {'dijametar': [], 'prosecan_stepen': [], 'prosecna_distanca': []}
    sum = 0
    for x, y in rezultati.items():
        for v in y:
            sum += v
        sum = sum / len(rezultati[x])
        prosek_rez[x].append(round(sum, 2))
        sum = 0
    
    return prosek_rez;

def analiza_mreze_klastera(mreza_klastera):
    broj_cvorova = mreza_klastera.number_of_nodes()
    broj_linkova = mreza_klastera.number_of_edges()
    broj_povezanih_komponenti = nx.number_connected_components(mreza_klastera)
    
    dijametar_mreze = nx.diameter(mreza_klastera) if broj_povezanih_komponenti == 1 else "beskonacna"
    prosecan_stepen_mreze = round(prosecan_stepen(mreza_klastera), 2)
    
    print(f"\n=>Broj cvorova u mrezi je {broj_cvorova}, broj linkova je {broj_linkova} i broj povezanih komponenti je {broj_povezanih_komponenti}")
    print(f"=>Vrednost dijametra mreze klastera je {dijametar_mreze}, a prosecan stepen je {prosecan_stepen_mreze}")
    
    
    