from abc import ABC, abstractmethod

class Galleta(ABC):

    @abstractmethod
    def comer(self):
        pass

class GalletaConPasas(Galleta):
    def comer(self):
        print("Que rico con pasas")

class GalletaConChispasDeChocolate(Galleta):
    def comer(self):
        print("Que rico con chispas de chocolate")

# galleta1 = Galleta()
# galleta1.comer()

galleta = GalletaConPasas()
galleta.comer()
