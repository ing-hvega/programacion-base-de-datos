class Galleta:
    def comer(self, sabor):
        print(f"Que rico {sabor}")

class GalletaConPasas(Galleta):
    def comer(self, sabor):
        print("Que rico con pasas")

    def desechar(self):
        print("Desechando las pasas")

class GalletaConLeche(Galleta):
    def comer(self, sabor):
        print("Que rico con leche")

    def agregar_azucar(self):
        self.sabor = "azucar"


gallet = Galleta()
gallet.comer()

gallet_con_pasas = GalletaConPasas()
gallet_con_pasas.comer()
gallet_con_pasas.desechar()