import random


def __parse__(string: str) -> list:
    string = "".join(i if i != ")" else i + " " for i in string)
    list_ = []
    nbr = ""
    s = 0
    for i in range(len(string)):
        i += s
        if i >= len(string):
            break
        if string[i] in "+-*/":
            if string[i] == "-" and not nbr:
                list_.append("-")
            elif string[i] == "-" and nbr:
                list_.append(float(nbr))
                for j in ("+", '-'):
                    list_.append(j)
                nbr = ''
            elif nbr:
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
    try:
        for i in range(len(list_)):
            if list_[i] == "-" and list_[i + 1] != '-':
                del list_[i]
                list_[i] = -list_[i]
            elif list_[i] == "-" == list_[i + 1]:
                del list_[i]
                del list_[i]
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
    print(liste)
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
    def randomize():
        string = ""
        for i in range(b := random.randint(10, 20) // 2):
            a = str(random.randint(-10, 10))
            operator = random.choice("+-*/") if i != b - 1 else ''
            string += a + operator
        return string
    print(a := randomize())
    # print(calculate("5^0-2+3+10-8^4/4/-6"))
    print(round(calculate(a), 4))
