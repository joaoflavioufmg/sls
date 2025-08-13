class Conta:
     def __init__(self, clientes, numero, saldo = 0):
         self.saldo = 0
         self.clientes = clientes
         self.numero = numero
         self.operacoes = []
         self.deposito(saldo)

     def resumo(self):
         print("CC N°{0:3d} Saldo: \
         {1:10.2f}".format(self.numero, self.saldo))

     def saque(self, valor):
         if self.saldo >= valor:
               self.saldo -= valor
               self.operacoes.append(["SAQUE", valor])

     def deposito(self, valor):
         self.saldo += valor
         self.operacoes.append(["DEPOSITO", valor])

     def extrato(self):
         print("Extrato CC N°{0:3d}\n".format(self.numero))
         for o in self.operacoes:
               print("%10s %10.2f" % (o[0],o[1]))
         print("\n    Saldo: %10.2f\n" % self.saldo)


class ContaEspecial(Conta):
     def __init__(self, clientes, numero, saldo = 0, limite=0):
         Conta.__init__(self, clientes, numero, saldo)
         self.limite = limite

     def saque(self, valor):
         if self.saldo + self.limite >= valor:
               self.saldo -= valor
               self.operacoes.append(["SAQUE", valor])
