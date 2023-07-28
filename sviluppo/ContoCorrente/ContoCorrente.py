    
class Conto():
    def __init__(self, nome, conto ):
        self.nome = nome
        self.conto = conto
        pass


class ContoCorrente(Conto):

    def __init__(self, nome, conto ,importo ):

        super().__init__(nome, conto)
        self.__saldo = importo

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self , importo):
        self.preleva(self.__saldo)
        self.deposita(importo)

    
    def descrizione(self):
        print (self.nome , self.conto, self.__saldo)
        
               
    def preleva(self , importo):
        self.__saldo = self.__saldo - importo 
        pass

    def deposita(self , importo):
        self.__saldo = self.__saldo + importo 
        pass

class GestoreContiCorrenti():
    @staticmethod
    def bonifico (sorgente, destinazione ,importo):
        sorgente.preleva(importo)
        destinazione.deposita(importo)
        



def listaConti(c):
    
    c.c1.descrizione()
    c.c2.descrizione()
    c.c3.descrizione()

def inizializza ():
    c1 = ContoCorrente("Maurizio", "123456" , 1000.90)
    c2 = ContoCorrente("Luciana", "123444" , 1300)
    c3 = ContoCorrente("Eleonora", "9998989" , 800)
    return (c1,c2,c3)



c1,c2,c3 = inizializza()

c1.saldo = 10000
c2.saldo = 20000
c1.descrizione()
c2.descrizione()

GestoreContiCorrenti.bonifico(c1,c2, 1000)
c1.descrizione()
c2.descrizione()


