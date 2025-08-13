class Calendario(object):

    meses = (31,28,31,30,31,30,31,31,30,31,30,31)

    def __init__(self, dia = 1, mes = 1, ano = 1900):
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano

    def ano_bisexto(self, a):
        if a % 4:
            # nao eh ano bisexto
            return 0;
        else:
            if a % 100:
                return 1;
            else:
                if a % 400:
                    return 0
                else:
                    return 1

    def set(self, dia, mes, ano):
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano

    def get():
        return (self, self.__dia, self.__mes, self.__ano)

    def avanca(self):

        meses = Calendario.meses
        max_dias = meses[self.__mes - 1]
        if self.__mes == 2:
            max_dias += self.ano_bisexto(self.__ano)
        if self.__dia == max_dias:
            self.__dia = 1
            if self.__mes == 12:
                self.__mes = 1
                self.__ano += 1
            else:
                self.__mes += 1
        else:
            self.__dia += 1

    def __str__(self):
        return str(self.__dia) + "/" + str(self.__mes) + "/" + str(self.__ano)

if __name__ == "__main__":
    x = Calendario()
    print(x)
    x.avanca()
    print(x)
    print()
