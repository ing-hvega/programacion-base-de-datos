class Galleta:

    def __init__(self, valor):
        self.valor = valor

    def comer(self):
        print(f"¡Estoy comiendo una galleta de {self.valor}!")

class GalletaNueva(Galleta):
    def agregar_leche(self):
        print("Agregando leche a la galleta")


galleta = Galleta("Vainilla")
galleta.comer()

galleta_nueva = GalletaNueva("Chocolate con leche")
galleta_nueva.agregar_leche()
galleta_nueva.comer()