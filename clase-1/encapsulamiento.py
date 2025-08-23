class Galleta:

    def __init__(self, valor):
        self.valor = valor

    def obtener_valor(self):
        return self.valor

    def cambiar_valor(self, nuevo_valor):

        if nuevo_valor > 20:
            self.valor = nuevo_valor
        else:
            print("El nuevo valor no puede ser menor a 20")

galleta = Galleta(10)

print(galleta.obtener_valor())

galleta.cambiar_valor(25)

print(galleta.obtener_valor())