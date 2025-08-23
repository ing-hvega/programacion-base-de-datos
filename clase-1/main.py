def operacoiones_matematicas():
    suma = 50 + 10
    rest = 50 - 10
    mult = 50 * 10
    div = 50 / 10

    print(f"La suma es: {suma}")


def concatenar_cadenas():
    nombre = "Pablo"

    saludo = "Hola " + nombre + " como estas?"

    print(f"{saludo}")


def listas():
    list = [1, 2, "A"]

    primer_elemento = list[2]

    print(f"El primer elemento de la lista es: {primer_elemento}")

def condicionales():
    numero = 20

    if numero > 10:
        print("El numero es mayor que 10")
    elif numero == 10:
        print("El numero es igual a 10")
    else:
        print("El numero es menor que 10")

def bucle_for():
    for i in range(10):
        print(i)

def bucle_while():
    contador = 1
    while contador <= 5:
        print(contador)
        contador += 1

if __name__ == "__main__":
    # operacoiones_matematicas()
    # concatenar_cadenas()
    # listas()
    # condicionales()
    # bucle_for()
    bucle_while()
