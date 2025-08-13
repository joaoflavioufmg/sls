class Relogio(object):

    def __init__(self, horas = 0, minutos = 0, segundos = 0):
        self.__horas = horas
        self.__minutos = minutos
        self.__segundos = segundos

    def set(self, horas, minutos, segundos = 0):
        self.__horas = horas
        self.__minutos = minutos
        self.__segundos = segundos

    def tic(self):
        """Tempo sera avancado em 1 segundo"""
        if self.__segundos == 59:
            self.__segundos = 0
            if self.__minutos == 59:
                self.__minutos = 0
                self.__horas = 0 if self.__horas == 23 else self.__horas + 1
            else:
                self.__minutos += 1
        else:
            self.__segundos += 1

    def mostra(self):
        print("%d:%d:%d" % (self.__horas, self.__minutos, self.__segundos))

    def __str__(self):
        return "%2d:%2d:%2d" % (self.__horas, self.__minutos, self.__segundos)

if __name__ == "__main__":
    x = Relogio()
    print(x)
    for i in range(10000):
        x.tic()
    print(x)
    print()
