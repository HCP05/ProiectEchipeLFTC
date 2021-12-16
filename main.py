class elementStivaLucru:
    isTerm = False
    index = None
    char = ''


def parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali):
    # Parametrii de lucru
    cod = "q"
    index = "0"
    stivaLucru = []
    stivaIntrare = [listaReguliProductie[0][0]]
    #


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

    inputDeVerificat = input("Verificati: ")

    parcurgere(inputDeVerificat, listaReguliProductie, nonTerminali)
