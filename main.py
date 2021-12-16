from enum import Enum


class codStatus(Enum):
    Q = 0,
    R = 1,
    T = 2,
    E = 3


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


def parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali):
    # Parametrii de lucru
    cod = codStatus.Q
    index = "0"
    stivaLucru = []
    stivaIntrare = [listaReguliProductie[0][0]]
    #

    while (True):
        match cod:
            case codStatus.Q:
                if isNonTerm(stivaIntrare[-1], nonTerminali):
                    stivaLucru.append(elementStivaLucru(False))


def citireListaProductie():
    nonTerminali = set()
    with open("input.txt", "r") as file:
        lines = file.readlines()
        rules = []

        for line in lines:
            line = line.strip()
            line = line.replace(' ', '')
            parts = line.split("->")
            nonTerminali.add(parts[0])
            rules.append(parts)
    return rules, nonTerminali


if __name__ == '__main__':
    listaReguliProductie, nonTerminali = citireListaProductie()
    print(listaReguliProductie)
    inputDeVerificat = input("Verificati: ")

    parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali)
