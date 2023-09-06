# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:14:27 2022

@author: Natasa
"""
import networkx as nx
import os

from ucitavanje_grafa import ucitaj_rucni_klasterabilan_graf, ucitaj_rucni_neklasterabilan_graf, \
ucitaj_random_graf, ucitaj_epinions_slashdot_graf, ucitaj_wiki_graf, prikazi_graf, prikazi_mrezu_klastera
from detekcija_klastera import pronadji_klastere, kreiraj_klastere, pronadji_koalicije_i_antikoalicije, \
    konstruisi_mrezu_klastera
from analiza import analiza_koalicija_i_antikoalicija, analiza_mreze_klastera

def main():
    graf = prikaziOpcije()
    broj_povezanih_komponenti = nx.number_connected_components(graf)
    print(f"\n=>Graf sadrzi {len(list(graf.nodes))} cvorova i {len(list(graf.edges))} linkova")
    print(f"=>Broj povezanih komponenti u grafu je {broj_povezanih_komponenti}")
    
    pozitivni_linkovi = [(u, v) for (u, v, d) in graf.edges(data=True) if d['label'] == "+"]
    negativni_linkovi = [(u, v) for (u, v, d) in graf.edges(data=True) if d['label'] == "-"]
    print(f"\nPozitivni linkovi {len(pozitivni_linkovi)}, negativni {len(negativni_linkovi)}")
    
    if broj_povezanih_komponenti == 1:
        print(f"=>Vrednost dijametra u grafu je {nx.diameter(graf)}")
    else:
        print("Posto je broj povezanih komponenti veci od 1 vrednost dijametra je beskonacna")
        
    lista_klastera = pronadji_klastere(graf)
    print(f"=>Broj klastera u grafu je {len(lista_klastera)}")
    
    if len(lista_klastera) < 15:
        for k in lista_klastera:
            print(k)
    klasteri = kreiraj_klastere(lista_klastera, graf.edges.data())
    
    if len(klasteri) < 15:
        prikazi = input("\n-->Da li zelite graficki prikaz klastera? (y, n): ")
        if(prikazi == "y" or prikazi == "Y"):
            i = 1
            for k in klasteri:
                prikazi_graf(k, "Klaster "+str(i))
                i += 1
    res = pronadji_koalicije_i_antikoalicije(klasteri)
    koalicije = res[0]
    antikoalicije = res[1]
    losi_linkovi = res[2]
    print(f"\n=>U grafu ima {len(koalicije)} koalicija i {len(antikoalicije)} antikoalicija")
    
    if len(antikoalicije) == 0:
        print("=>Posto u grafu nema antikoalicija znaci da je graf klasterabilan.")
    else:
        print("=>Posto u grafu imamo antikoalicija znaci da graf nije klasterabilan.")
    
    if len(koalicije) < 11 and len(antikoalicije) < 11:
        prikazi = input("\n-->Da li zelite prikaz klastera koalicije i antikoalocije? (y, n): ")
        if(prikazi == "y" or prikazi == "Y"):
            if len(koalicije) > 0:
                print("\n=>Klasteri koji su koalicija su:")
                for k in koalicije:
                    print(k.nodes)
            else:
                print("Nema klastera koji su koalicija")
                
            if len(antikoalicije) > 0:
                print("\n==>Klasteri koji su antikoalicija su:")
                for k in antikoalicije:
                    print(k.nodes)
            else:
                print("Nema klastera koji su antikoalicija")
            
    if len(antikoalicije) > 0:
        print(f"\n=>Da bi mreza bila klasterabilna broj linkova koje je potrebno ukloniti iz grafa je {len(losi_linkovi)}")
        if len(losi_linkovi) < 100:
            print("To su:")
            for l in losi_linkovi:
                print(l)
        else:
            print("Prvih 100 losih linkova:")
            i = 0
            while i <= 100:
                print(losi_linkovi[i])
                i += 1
                
    print("\n=====Analiza koalicija i antikoalicija=====\n")
    analiza_koalicija_i_antikoalicija(koalicije, antikoalicije)   
       
    mreza_klastera = konstruisi_mrezu_klastera(graf, klasteri)
    if mreza_klastera != None:
        print("\n=>Mreza klastera je kreirana")
        if len(mreza_klastera.nodes) < 50:
            prikazi_mrezu_klastera(mreza_klastera, "Mreza klastera")
        
        print("\n=====Analiza mreze klastera=====")
        analiza_mreze_klastera(mreza_klastera) 
        
    print("\n=============== KRAJ PROGRAMA! ===============")
    
def prikaziOpcije():
    print("\nUnesite broj u zavisnosti od toga koji graf zelite da ucitate:")
    print("1: Rucno napravljen klasterabilan graf")
    print("2: Rucno napravljen neklasterabilan graf")
    print("3: Random generisan graf")
    print("4: Graf napravljen na osnovu realnih mreza")
    print("5: Kraj programa")
    
    opcija = "0"
    while int(opcija) < 1 or int(opcija) > 5:
        opcija = input("\nUnesite opciju: ")
    switcher = {
        1: rucni_klast_graf,
        2: rucni_neklast_graf,
        3: random_graf,
        4: realna_mreza_graf}
    
    izabrano = switcher.get(int(opcija))
    return izabrano();

def rucni_klast_graf():
    return ucitaj_rucni_klasterabilan_graf();

def rucni_neklast_graf():
    return ucitaj_rucni_neklasterabilan_graf();

def random_graf():
    return ucitaj_random_graf();

def realna_mreza_graf():
    print("\nUnesite broj u zavisnosti za koji fajl zelite da ucitate graf:")
    print("1: Iz fajla 'soc-sign-epinions'")
    print("2: Iz fajla 'soc-sign-Slashdot090221'")
    print("3: Iz fajla 'wiki-RfA'")
    
    opcija = "0"
    while int(opcija) < 1 or int(opcija) > 3:
        opcija = input("\nUnesite opciju: ")
    parent = os.path.abspath(os.path.dirname(__file__))
    match opcija:
        case "1":
            return ucitaj_epinions_slashdot_graf(os.path.join(parent, "Realne mreze", "soc-sign-epinions.txt"))
        case "2":
            return ucitaj_epinions_slashdot_graf(os.path.join(parent, "Realne mreze", "soc-sign-Slashdot090221.txt"))
        case "3":
            return ucitaj_wiki_graf(os.path.join(parent, "Realne mreze", "wiki-RfA.txt"))

if __name__ == "__main__":
    main()