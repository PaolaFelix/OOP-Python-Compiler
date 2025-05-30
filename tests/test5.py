def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b != 0:
        return a / b
    else:
        return None

# Uso
print(sumar(5, 3))       # 8
print(dividir(10, 0))    # None
