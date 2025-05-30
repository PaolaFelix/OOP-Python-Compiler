def crear_vehiculo(marca, modelo, velocidad=0):
    return {"marca": marca, "modelo": modelo, "velocidad": velocidad}

def acelerar(vehiculo, incremento):
    vehiculo["velocidad"] += incremento

def frenar(vehiculo, decremento):
    vehiculo["velocidad"] = max(0, vehiculo["velocidad"] - decremento)

# Uso
mi_carro = crear_vehiculo("Toyota", "Corolla")
acelerar(mi_carro, 30)
frenar(mi_carro, 10)
print(mi_carro)  # {'marca': 'Toyota', 'modelo': 'Corolla', 'velocidad': 20}
