

def suma02(a,b):
 return a + b


def producto(a, b):
 return a * b


def potencia(a, b):
 return a ** b


def division(numerador, divisor):
   if divisor != 0:
       division = numerador / divisor
       entera = numerador // divisor
       resto = numerador % divisor
       return f"División real: {division}, entera: {entera}, resto: {resto}"
   else:
       return "Error: No se puede dividir por cero"
