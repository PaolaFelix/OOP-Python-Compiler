# Función para crear una cuenta bancaria
def crear_cuenta(nombre, saldo_inicial):
    return {"nombre": nombre, "saldo": saldo_inicial}

# Función para depositar dinero
def depositar(cuenta, cantidad):
    cuenta["saldo"] += cantidad

# Función para retirar dinero
def retirar(cuenta, cantidad):
    if cuenta["saldo"] >= cantidad:
        cuenta["saldo"] -= cantidad
    else:
        print("Saldo insuficiente")

# Uso
cuenta_juan = crear_cuenta("Juan", 1000)
depositar(cuenta_juan, 500)
retirar(cuenta_juan, 300)
print(cuenta_juan)  # {'nombre': 'Juan', 'saldo': 1200}
