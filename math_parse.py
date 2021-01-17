

def __parse__(string: str) -> list:
	list_ = []
	nbr = ""
	for i in range(len(string)):
		if string[i] in "+-*/":
			if nbr != "":
				list_.append(float(nbr))
				list_.append(string[i])
				nbr = ""
		elif string[i].isdigit():
			nbr += string[i]
		if i == len(string) - 1 and nbr != "":
			list_.append(float(nbr))
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

if __name__ == '__main__':
	print(calculate("5*5*5*5/5/5 + 20 - 20 + 1000/5^3"))