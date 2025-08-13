# Atributos: Public, Protected e Private
# Nomenclatura: Tipo        : Significado
# nome          Public      Atributos livremente acessados fora da classe
# _nome         Protected   Atributos nao podem ser usados fora da classe a menos que seja numa subclasse
# __nome        Private     Atributos invisiveis e inacessiveis. Acesso proibido. Somente dentro da propria classe

class A():

    def __init__(self):
        self.__priv = "Eu sou Private"
        self._prot = "Eu sou Protected"
        self.pub = "Eu sou Public"
