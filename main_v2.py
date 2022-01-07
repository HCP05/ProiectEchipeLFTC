import sys
from enum import Enum

TOKENS = {
    0: "ID",
    1: "CONST"
}

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

def verificare(fip_element, grammar_element, atoms):
    #print("Checking %d and %s, in tokens %s"%(fip_element[0],
    #    grammar_element, str(fip_element[0] in TOKENS)))


    if fip_element[0] in TOKENS:
        return TOKENS[fip_element[0]] == grammar_element
    else:
        fip_string = atoms[fip_element[0]]

        return grammar_element[0] == "'" and\
                fip_string == grammar_element[1:-1]

def findRelativeIndex(rule, all_rules):
    return rule.index - findIndex(rule.char, all_rules)

def parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali,
        atomi):
    # Parametrii de lucru
    cod = codStatus.Q
    index = 0
    stivaLucru = []
    stivaIntrare = [listaReguliProductie[0][0]]
    #
    max_len = 0

    while (True):
        #print(cod)
        #print([[el.char, el.isTerm, el.index] for el in stivaLucru])

        #if len(stivaLucru) >= max_len:
        #    print(str(index) + ": " + str([el.char +
        #        (str(findRelativeIndex(el, listaReguliProductie))
        #        if el.index != None else "") for el in
        #        stivaLucru]))
        #    print(stivaIntrare)
        max_len = max(max_len, len(stivaLucru))
        #print("Input: " + str(stivaIntrare))

        if cod == codStatus.Q:
            if len(stivaIntrare):
                element = stivaIntrare[-1]

                if isNonTerm(element, nonTerminali): # expandare
                    indexRegula = findIndex(element, listaReguliProductie)

                    stivaLucru.append(elementStivaLucru(False,
                        indexRegula, element))
                    stivaIntrare.pop()
                    stivaIntrare.extend(listaReguliProductie[indexRegula][1][::-1])
                elif index < len(inputDeVerificat) and verificare(
                        inputDeVerificat[index], element, atomi): # avans
                    index += 1
                    stivaIntrare.pop()
                    stivaLucru.append(elementStivaLucru(True, None,
                        element))
                else: # insucces de moment
                    cod = codStatus.R
            elif index < len(inputDeVerificat):
                cod = codStatus.R
            else: # success
                prodList = []
                for element in stivaLucru:
                    if not element.isTerm:
                        prodList.append(element.char +
                                str(findRelativeIndex(element,
                                    listaReguliProductie)))

                print(prodList)

                #print("success returning")
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
                    if lungime:
                        stivaIntrare = stivaIntrare[0:-lungime]
                    stivaIntrare.extend(listaReguliProductie[indexRegula][1][::-1])
                elif index == 0 and elementLucru.char == listaReguliProductie[0][0]: # eroare
                    #print("failure returning")
                    return -1
                else: # comprimare
                    lungime = len(listaReguliProductie[elementLucru.index][1])
                    stivaIntrare = stivaIntrare[0:-lungime]
                    stivaIntrare.append(elementLucru.char)

def citireListaProductie(file_name):
    nonTerminali = set()
    with open(file_name, "r") as file:
        lines = file.readlines()
        rules = []

        for line in lines:
            line = line.strip()

            if not len(line):
                continue

            parts = line.split("->")
            rule_name = parts[0].strip()
            terms = parts[1].split()

            if rule_name == terms[0]:
                print("Gramatica recursiva la stanga, nu se poate analiza")
                return None, None

            if '%empty' in terms:
                terms = []

            nonTerminali.add(rule_name)

            rules.append([rule_name, terms])
    return rules, nonTerminali

def citireAtomi(file_name):
    atomi = []

    with open(file_name, "r") as file:
        atomi = [line.strip() for line in file.readlines()]

    return atomi

def citireFIP(file_name):
    fip = []

    with open(file_name, "r") as file:
        lines = file.readlines()

        for line in lines:
            parts = line.split()

            code = int(parts[0])
            symbol_id = int(parts[1])

            fip.append([code, symbol_id])

    return fip

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Usage: %s <grammar_file> <atoms_file> <input_file>"%(
            sys.argv[0]))
        sys.exit(1)

    grammar_file = sys.argv[1]
    atoms_file = sys.argv[2]
    input_file = sys.argv[3]

    listaReguliProductie, nonTerminali =\
        citireListaProductie(grammar_file)

    if listaReguliProductie == None:
        sys.exit(1)

    atomi = citireAtomi(atoms_file)

    #print(atomi)

    #print(listaReguliProductie)
    inputDeVerificat = citireFIP(input_file)

    index = parcurgere(inputDeVerificat, listaReguliProductie,
            nonTerminali, atomi)

    if index == len(inputDeVerificat):
        print("Secventa acceptata")
    else:
        print("Secventa respinsa")
