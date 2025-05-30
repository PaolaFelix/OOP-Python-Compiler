class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.velocidad = 0

    def acelerar(self, incremento):
        self.velocidad += incremento

    def frenar(self, decremento):
        self.velocidad = max(0, self.velocidad - decremento)

    def __str__(self):
        return f"{self.marca} {self.modelo} a {self.velocidad} km/h"

# Uso
mi_carro = Vehiculo("Toyota", "Corolla")
mi_carro.acelerar(30)
mi_carro.frenar(10)
print(mi_carro)  # Toyota Corolla a 20 km/h
