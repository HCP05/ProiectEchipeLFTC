import sys
from enum import Enum

class codStatus(Enum):
    Q = 0,
    R = 1

class elementStivaLucru:
    isTerm = False
    index = None
    char = ''

    def __init__(self, isTerm, index, char):
        self.index = index
        self.isTerm = isTerm
        self.char = char

def isNonTerm(x: str, listTerm: set):
    return x in listTerm

def findIndex(nonTerm, listaReguliProductie, minIndex = -1):
    for index, element in enumerate(listaReguliProductie):
        if element[0] == nonTerm and index > minIndex:
            return index
    
    return -1

def parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali):
    # Parametrii de lucru
    cod = codStatus.Q
    index = 0
    stivaLucru = []
    stivaIntrare = [listaReguliProductie[0][0]]
    #

    while (True):
        #print(cod)
        #print([[el.char, el.isTerm, el.index] for el in stivaLucru])
        #print(stivaIntrare)

        if cod == codStatus.Q:
            if len(stivaIntrare):
                element = stivaIntrare[-1]

                if isNonTerm(element, nonTerminali): # expandare
                    indexRegula = findIndex(element, listaReguliProductie)

                    stivaLucru.append(elementStivaLucru(False,
                        indexRegula, element))
                    stivaIntrare.pop()
                    stivaIntrare.extend(listaReguliProductie[indexRegula][1][::-1])
                elif index < len(inputDeVerificat) and inputDeVerificat[index] == element: # avans
                    index += 1
                    stivaIntrare.pop()
                    stivaLucru.append(elementStivaLucru(True, None,
                        element))
                else: # insucces de moment
                    cod = codStatus.R
            else: # success
                prodList = []
                for element in stivaLucru:
                    if not element.isTerm:
                        prodList.append(element.char +
                                str(element.index))

                print(prodList)

                return index
        elif cod == codStatus.R:
            elementLucru = stivaLucru.pop()

            if elementLucru.isTerm: # revenire
                index -= 1
                stivaIntrare.append(elementLucru.char)
            else: # alta incercare
                indexRegula = findIndex(elementLucru.char,
                        listaReguliProductie, elementLucru.index)

                if indexRegula != -1: # urmatoarea regula
                    cod = codStatus.Q
                    stivaLucru.append(elementStivaLucru(False,
                        indexRegula, elementLucru.char))

                    lungime = len(listaReguliProductie[elementLucru.index][1])
                    stivaIntrare = stivaIntrare[0:-lungime]
                    stivaIntrare.extend(listaReguliProductie[indexRegula][1][::-1])
                elif index == 0 and elementLucru.char == listaReguliProductie[0][0]: # eroare
                    return -1
                else: # comprimare
                    lungime = len(listaReguliProductie[elementLucru.index][1])
                    stivaIntrare = stivaIntrare[0:-lungime]
                    stivaIntrare.append(elementLucru.char)

def citireListaProductie():
    nonTerminali = set()
    with open("input.txt", "r") as file:
        lines = file.readlines()
        rules = []

        for line in lines:
            line = line.strip()
            line = line.replace(' ', '')
            parts = line.split("->")

            if parts[0] == parts[1][0]:
                print("Gramatica recursiva la stanga, nu se poate analiza")
                return None, None

            nonTerminali.add(parts[0])

            charList = [char for char in parts[1]]
            rules.append([parts[0], charList])
    return rules, nonTerminali

if __name__ == '__main__':
    listaReguliProductie, nonTerminali = citireListaProductie()
    
    if listaReguliProductie == None:
        sys.exit(1)

    #print(listaReguliProductie)
    inputDeVerificat = input("Verificati: ")

    index = parcurgere(inputDeVerificat, listaReguliProductie,
            nonTerminali)

    if index == len(inputDeVerificat):
        print("Secventa acceptata")
    else:
        print("Secventa respinsa")
