def __parse__(string: str) -> list:
    string = "".join(i if i != ")" else i + " " for i in string)
    list_ = []
    nbr = ""
    s = 0
    for i in range(len(string)):
        i += s
        if i >= len(string):
            break
        if string[i] in "+-*/^":
            if string[i] == "-":
                list_.append('-')
            elif nbr != "":
                list_.append(float(nbr))
                list_.append(string[i])
                nbr = ""
        elif string[i] == "(":
            a = __count__(string[i:]) + i
            calculation = calculate(string[i + 1:a])
            s += len(string[i: a])
            nbr = float(calculation)
        elif string[i].isdigit() or string[i] == ".":
            nbr += string[i]
        if i == len(string) - 1 and nbr != "":
            list_.append(float(nbr))
    nbr = ''
    for i in range(len(list_)):
        try:
            if list_[i] == "-":
                del list_[i]
                list_[i] = -list_[i]
        except:
            pass
    return list_


def __subcalc__(liste, dico: dict):
    counter = 0
    for i in range(len(liste)):
        i -= counter
        if liste[i] in list(dico.keys()):
            nbr = dico[liste[i]].__call__(liste[i - 1], liste[i + 1])
            for _ in range(3):
                del liste[i - 1]
            liste.insert(i - 1, nbr)
            counter += 2


def calculate(string: str) -> int:
    liste = __parse__(string)
    __subcalc__(liste, {"^": float.__pow__})
    __subcalc__(liste, {"*": float.__mul__, "/": float.__truediv__})
    __subcalc__(liste, {"+": float.__add__, "-": float.__sub__})
    return int(liste[0]) if liste[0].is_integer() else liste[0]


def __count__(n):
    a = 0
    for j in range(len(n)):
        if n[j] == ")":
            a -= 1
        elif n[j] == "(":
            a += 1
        if n[j] == ")" and a == 0:
            break
    return j


if __name__ == '__main__':
    print(calculate("((-1*3) + 6.7)"))
