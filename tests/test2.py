class CuentaBancaria:
    def __init__(self, nombre, saldo_inicial):
        self.nombre = nombre
        self.saldo = saldo_inicial

    def depositar(self, cantidad):
        self.saldo += cantidad

    def retirar(self, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
        else:
            print("Saldo insuficiente")

    def mostrar_saldo(self):
        print(f"Cuenta de {self.nombre}, saldo: {self.saldo}")

# Uso
cuenta_juan = CuentaBancaria("Juan", 1000)
cuenta_juan.depositar(500)
cuenta_juan.retirar(300)
cuenta_juan.mostrar_saldo()  # Cuenta de Juan, saldo: 1200
