from abc import ABC, abstractmethod


# Clase abstracta
class UsuarioBase(ABC):

    def __init__(self, nombre, correo):
        self._nombre = nombre
        self._correo = correo

    @abstractmethod
    def mostra_info(self):
        pass

    # GETTERS Y SETTERS
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def correo(self):
        return self._correo


# Herencia y Polimorfismo
class UsuarioNormal(UsuarioBase):
    def mostra_info(self):
        print(f"Nombre: {self.nombre} \nCorreo: {self.correo}")

class UsuarioAdmin(UsuarioBase):
    def mostra_info(self):
        print(f"Nombre: {self.nombre} \nCorreo: {self.correo} \nEs administrador")


class GestorUsuarios:
    def __init__(self):
        self.usuarios = []

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)


gestor = GestorUsuarios()
# usuario = UsuarioNormal("Pablo", "p@gmail.om")
# usuario.mostra_info()

def mostrar_menu():
    print("1. Crear usuario")
    print("2. Mostrar usuarios")
    print("3. Salir")

    return input("Seleccione una opcion: ")


while True:
    opcion = mostrar_menu()

    if opcion == "1":
        nombre = input("Ingrese el nombre del usuario: ")
        correo = input("Ingrese el correo del usuario: ")
        gestor.agregar_usuario(UsuarioNormal(nombre, correo))

    elif opcion == "2":
        for usuario in gestor.usuarios:
            usuario.mostra_info()
    elif opcion == "3":
        break
    else:
        print("Opcion no valida, Intente de nuevo.")
