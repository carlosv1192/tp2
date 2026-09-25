"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico Nro. 1 — Sistema de gestión de ventas: Kiosco "El Campus"

Integrantes del grupo:
    - Becerra, Facundo Daniel
    - Vallejos, Carlos
"""

"""
Acá declaramos acumuladores, contadores y constantes para usar en 
el programa principal.
"""
MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito
CATEGORIAS = ["Golosinas", "Bebidas", "Almacén", "Librería"]
MEDIOS_PAGO = ["Efectivo", "Débito", "Crédito"]
STOCK_MINIMO = 5 # por debajo de este, el producto va a reposición
CODIGO, NOMBRE, CATEGORIA, PRECIO, STOCK = 0, 1, 2, 3, 4
NUMERO, CODIGO_VENTA, CANTIDAD, MEDIO_PAGO, IMPORTE_FINAL = 0, 1, 2, 3, 4

total_recaudado = 0
cantidad_ventas = 0
venta_mas_alta = 0
total_golosinas = 0
total_bebidas = 0
total_almacen = 0
total_libreria = 0
cantidad_efectivo = 0
cantidad_debito = 0
cantidad_credito = 0

#CATÁLOGO INICIAL
# Lista de productos. Cada producto es una LISTA (mutable: el stock cambia):
#     [codigo, nombre, categoria, precio, stock]
# NO está ordenado por código: ordenarlo al iniciar el
# programa es parte del trabajo (y condición para la búsqueda binaria).
# =====================================================================
def catalogo_inicial():
    """Devuelve el catálogo de partida del kiosco (lista de listas).
    Pre: 
    Post: devuelve una lista de productos
    """
    return [
        [305, "Alfajor triple",           1, 1500.0, 24],
        [112, "Agua saborizada 500 ml",   2, 1900.0, 10],
        [421, "Cuaderno",                 4, 10000.0, 15],
        [208, "Galletitas surtidas",      3, 2800.0,  8],
        [117, "Gaseosa 1.5 L",            2, 4000.0,  6],
        [302, "Chicles",                  1,  700.0, 40],
        [415, "Birome azul",              4, 1200.0,  3],
        [210, "Fideos 500 g",             3, 2100.0, 12],
        [310, "Chocolate con leche",      1, 3200.0,  4],
        [119, "Jugo en polvo",            2,  900.0, 30],
    ]

def buscar_por_codigo(catalogo, codigo):
    """Busca un producto por código con BÚSQUEDA BINARIA.

    Pre:  catalogo es una lista de productos ORDENADA por código (ascendente).
    Post: devuelve la posición del producto con ese código, o -1 si no está.
          No modifica el catálogo.

    Es la búsqueda binaria de la Clase 8, adaptada: en lugar de comparar el
    elemento completo, se compara el campo CODIGO de cada producto.
    """
    izq = 0
    der = len(catalogo) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if catalogo[medio][CODIGO] == codigo:
            return medio
        if catalogo[medio][CODIGO] > codigo:
            der = medio - 1
        else:
            izq = medio + 1
    return -1

def formato_de_precio(valor):
    """Establece el tipeo de moneda argentina a un número: 2 decimales, punto de
    miles y coma decimal.
    Pre:  valor es un número.
    Post: devuelve un string con el valor formateado, sin el signo '$'.
    """
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return texto

def pedir_entero_en_rango(mensaje, minimo, maximo):
    """Solicita al usuario un número entero dentro de un rango, reintentando
    hasta que la entrada sea correcta dentro de los límites establecidos.
    Si es una cadena de texto que no representa un número entero, se rechaza
    y se pide reingresar el dato.
    Recibe:  mensaje (str) a mostrar, minimo (int) y maximo (int) del rango.
    Devuelve: el número ingresado (int), garantizado dentro del rango.
    """
    entrada = input(mensaje)
    while not entrada.isdigit() or not (minimo <= int(entrada) <= maximo):
        print(f"Entrada inválida. Ingrese un número entero entre {minimo} y {maximo}.")
        entrada = input(mensaje)
    return int(entrada)

def pedir_real_en_rango(mensaje, minimo):
    """Solicita al usuario un número real estrictamente mayor que un mínimo,
    reintentando hasta que la entrada sea válida.
    Validamos que sea un número real quitando el punto que tenga con el replace
    para que queden solo los dígitos; se verifica si es un número con isdigit()
    y, finalmente, se convierte a float para comparar con el mínimo.
    Recibe:  mensaje (str) a mostrar y minimo (float) que es el valor a superar.
    Devuelve: el número ingresado (float), garantizado mayor que 'minimo'.
    """
    entrada = input(mensaje)
    while not entrada.replace('.', '', 1).isdigit() or not (minimo < float(entrada)):
        print(f"Entrada inválida. Ingrese un número real mayor que {minimo}.")
        entrada = input(mensaje)
    return float(entrada)

def registrar_venta():
    """
    Sirve para registrar una venta a partir de datos pedidos al usuario.
    Recibe: nada.
    Devuelve: nada, solo imprime el tique de la venta y actualiza los contadores
    del día con lo de esta venta.
    """
    global total_golosinas, total_bebidas, total_almacen, total_libreria
    global cantidad_efectivo, cantidad_debito, cantidad_credito
    categoria = categoria_producto()
    precio_unitario = pedir_real_en_rango("Ingrese el precio unitario del producto: ", 0)
    cantidad_unidades = pedir_entero_en_rango("Ingrese la cantidad de unidades: ", 1, 9999)
    medio_de_pago = pedir_entero_en_rango("Ingrese el medio de pago (1: Efectivo, 2: Tarjeta de débito, 3: Tarjeta de crédito): ", 1, 3)
    subtotal = calcular_subtotal(precio_unitario, cantidad_unidades)
    descuento_monto = calcular_descuento_por_monto(subtotal)
    ajuste_medio_pago = calcular_ajuste_medio_pago(subtotal, descuento_monto, medio_de_pago)
    importe_final = calcular_importe_final(subtotal, descuento_monto, ajuste_medio_pago)
    codigo_suerte = obtener_codigo_suerte(round(importe_final))
    generar_tique(precio_unitario, cantidad_unidades, categoria, subtotal, descuento_monto, ajuste_medio_pago, medio_de_pago, importe_final, codigo_suerte)
    #A continuación, actualizamos los acumuladores del día con lo de esta venta.
    actualizar_contadores_de_venta(importe_final, categoria, medio_de_pago)

def actualizar_contadores_de_venta(importe_final, categoria, medio_de_pago):
    """
    Sirve para actualizar los contadores y acumuladores del día con lo de la venta recién registrada.
    Recibe: el importe final, la categoría del producto y el medio de pago.
    Devuelve: nada, ya que solo actualiza los contadores.
    """
    global total_recaudado, cantidad_ventas, venta_mas_alta
    global total_golosinas, total_bebidas, total_almacen, total_libreria
    global cantidad_efectivo, cantidad_debito, cantidad_credito

    total_recaudado = total_recaudado + importe_final   
    cantidad_ventas = cantidad_ventas + 1
    if importe_final > venta_mas_alta:
        venta_mas_alta = importe_final
    if categoria == 1:
        total_golosinas = total_golosinas + importe_final
    elif categoria == 2:
        total_bebidas = total_bebidas + importe_final
    elif categoria == 3:
        total_almacen = total_almacen + importe_final
    else:
        total_libreria = total_libreria + importe_final
    if medio_de_pago == 1:
        cantidad_efectivo = cantidad_efectivo + 1
    elif medio_de_pago == 2:
        cantidad_debito = cantidad_debito + 1
    else:
        cantidad_credito = cantidad_credito + 1

def nombre_de_categoria(categoria):
    """Sirve para pasar el número de categoría correspondiente
    a su denominación textual y evitar que escriba solo el número, que es
    menos legible y más difícil de asociar.
    Recibe: categoria (int) entre 1 y 4.
    Devuelve: el nombre de la categoría correspondiente como cadena.
    """
    match categoria:
        case 1:
            return "Golosinas"
        case 2:
            return "Bebidas"
        case 3:
            return "Almacén"
        case 4:
            return "Librería"

def nombre_de_medio_de_pago(medio_de_pago):
    """Traduce el número del medio de pago correspondiente
    a su denominación textual; evita que escriba solo el número, que es
    menos legible y más difícil de asociar.
    Recibe: medio_de_pago (int) entre 1 y 3.
    Devuelve: el nombre del medio de pago correspondiente como cadena.
    """
    match medio_de_pago:
        case 1:
            return "Efectivo"
        case 2:
            return "Tarjeta de débito"
        case 3:
            return "Tarjeta de crédito"

def calcular_subtotal(precio_unitario, cantidad_unidades):
    """Calcula el subtotal de la venta.
    Recibe: el precio unitario y la cantidad de unidades.
    Devuelve: el subtotal.
    """
    return precio_unitario * cantidad_unidades

def calcular_descuento_por_monto(subtotal):
    """Calcula el descuento por superar el monto mínimo. Si no lo supera,
    el descuento es 0.
    Recibe: el subtotal de la venta.
    Devuelve: el descuento, que puede ser 0.
    """
    if subtotal > MONTO_MINIMO_DESCUENTO:
        return subtotal * PORCENTAJE_DESCUENTO_MONTO / 100
    return 0

def calcular_ajuste_medio_pago(subtotal, descuento_monto, medio_de_pago):
    """Calcula el ajuste según el medio de pago (descuento o recargo),
    ya sobre el importe con el descuento por monto aplicado.
    Recibe: el subtotal, el descuento por monto y el medio de pago.
    Devuelve: el ajuste, que puede ser negativo (descuento) o positivo (recargo).
    """
    importe_tras_descuento = subtotal - descuento_monto
    if medio_de_pago == 1: #O sea, para efectivo.   
        return -(importe_tras_descuento * PORCENTAJE_DESCUENTO_EFECTIVO / 100)
    elif medio_de_pago == 3: #O sea, para crédito.    
        return importe_tras_descuento * PORCENTAJE_RECARGO_CREDITO / 100
    return 0 #Es el caso del débito, que no tiene ajuste ni recargo.

def calcular_importe_final(subtotal, descuento_monto, ajuste_medio_pago):
    """Calcula el importe final de la venta, combinando el subtotal,
    el descuento por monto y el ajuste por medio de pago.
    Recibe: subtotal, descuento por monto y ajuste por medio de pago.
    Devuelve: el importe final de la venta (a pagar).
    """
    return subtotal - descuento_monto + ajuste_medio_pago

def sumar_digitos(numero):
    """Es para resolver el cálculo auxiliar del código de la suerte.
    Recibe: un número entero positivo.
    Devuelve: la suma de sus dígitos, calculada recursivamente.
    """
    if numero == 0:
        return 0
    return numero % 10 + sumar_digitos(numero // 10)

def obtener_codigo_suerte(numero):
    """Sirve para calcular el código de la suerte que don Ramón le da
    al cliente en el final del tique. Toma los dígitos del importe final 
    de la venta como entero y los suma recursivamente hasta lograr 
    un solo dígito. Se apoya en la función sumar_digitos para hacer los cálculos 
    auxiliares.
    Recibe: un número entero positivo.
    Devuelve: un número entero entre 0 y 9, que es el código de la suerte.
    """
    if numero < 10:
        return numero
    return obtener_codigo_suerte(sumar_digitos(numero))

def categoria_producto():
    """Solicita al usuario la categoría del producto y devuelve el número
    correspondiente a la categoría elegida.
    Recibe: nada.
    Devuelve: un número entero entre 1 y 4, que representa la categoría."""
    print("Seleccione la categoría del producto: ")
    print("1) Golosinas")
    print("2) Bebidas")
    print("3) Almacén")
    print("4) Librería")
    categoria = pedir_entero_en_rango("Ingrese el número de la categoría: ", 1, 4)
    return categoria

def generar_tique(precio_unitario, cantidad_unidades, categoria, subtotal, descuento_monto, ajuste_medio_pago, medio_de_pago, importe_final, codigo_suerte):
    """Muestra el tique de la venta en detalle. Simplemente imprime
    ordenadamente los valores que ya vienen calculados.
    Recibe: precio unitario, cantidad de unidades, categoría, subtotal, descuento por monto, ajuste por medio de pago,
    medio de pago, importe final y código de la suerte.
    Devuelve: nada, solo imprime en pantalla.
    """
    print("===== TIQUE DE VENTA =====")
    print(f"Subtotal: ${round(subtotal, 2)}")
    if descuento_monto > 0:
        print(f"Descuento por monto ({PORCENTAJE_DESCUENTO_MONTO}%): -${round(descuento_monto, 2)}")
    print(f"Medio de pago: {nombre_de_medio_de_pago(medio_de_pago)}")
    if ajuste_medio_pago < 0:
        print(f"Descuento por pago en efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}%): -${round(abs(ajuste_medio_pago), 2)}")
    elif ajuste_medio_pago > 0:
        print(f"Recargo por pago con crédito ({PORCENTAJE_RECARGO_CREDITO}%): +${round(ajuste_medio_pago, 2)}")
    print(f"Compró {nombre_de_categoria(categoria)}, {cantidad_unidades} unidades por ${round(precio_unitario, 2)} cada una.")
    print(f"IMPORTE FINAL: ${round(importe_final, 2)}")
    print(f"Código de la suerte: {codigo_suerte}")
    print("========================")        

def pedir_confirmacion(mensaje):
    """Pide S/N al usuario, reintentando hasta que responda una de las dos.
    Recibe: mensaje (str) a mostrar.
    Devuelve: un booleano. True si respondió S, False si respondió N.
    """
    respuesta = input(mensaje).strip().upper()
    while respuesta != "S" and respuesta != "N":
        print("Entrada inválida. Responda 'S' para sí o 'N' para no.")
        respuesta = input(mensaje).strip().upper()
    return respuesta == "S"

def calcular_promedio_venta(total_recaudado, cantidad_ventas):
    """Calcula el importe promedio por venta, sin dividir por cero
    si todavía no hay ventas.
    Recibe: total recaudado y cantidad de ventas.
    Devuelve: el promedio de venta o 0 si no hay ventas.
    """
    if cantidad_ventas == 0:
        return 0
    return total_recaudado / cantidad_ventas

def determinar_medio_mas_utilizado(cant_efectivo, cant_debito, cant_credito):
    """Devuelve el nombre del medio de pago más utilizado en el día.
    Predeterminadamente, toma como mayor a la cantidad de efectivo, las compara
    con las de débito y crédito y devuelve el nombre del que tenga la mayor cantidad.
    Recibe: cantidad de ventas en efectivo, débito y crédito.
    Devuelve: el nombre del medio de pago más utilizado.
    """
    mayor = cant_efectivo
    nombre = "Efectivo"
    if cant_debito > mayor:
        mayor = cant_debito
        nombre = "Tarjeta de débito"
    if cant_credito > mayor:
        mayor = cant_credito
        nombre = "Tarjeta de crédito"
    return nombre

def mostrar_resumen_dia():
    """Muestra el resumen de ventas del día. No calcula nada directamente,
    usa calcular_promedio_venta y determinar_medio_mas_utilizado para eso.
    Recibe: nada.
    Devuelve: nada, solo imprime en pantalla.
    """
    print("***********************")
    print("=== RESUMEN DEL DÍA ===")
    if cantidad_ventas == 0:
        print("Todavía no se registraron ventas en el día.")
        return
    promedio = calcular_promedio_venta(total_recaudado, cantidad_ventas)
    medio_mas_usado = determinar_medio_mas_utilizado(cantidad_efectivo, cantidad_debito, cantidad_credito)
    print(f"Cantidad de ventas: {cantidad_ventas}")
    print(f"Total recaudado: ${round(total_recaudado, 2)}")
    print(f"Importe promedio por venta: ${round(promedio, 2)}")
    print(f"Venta más alta del día: ${round(venta_mas_alta, 2)}")
    print(f"Total en Golosinas: ${round(total_golosinas, 2)}")
    print(f"Total en Bebidas: ${round(total_bebidas, 2)}")
    print(f"Total en Almacén: ${round(total_almacen, 2)}")
    print(f"Total en Librería: ${round(total_libreria, 2)}")
    print(f"Ventas en efectivo: {cantidad_efectivo}")
    print(f"Ventas con débito: {cantidad_debito}")
    print(f"Ventas con crédito: {cantidad_credito}")
    print(f"Medio de pago más utilizado: {medio_mas_usado}")
    print("***********************")

def cuenta_regresiva(numero):
    """Cuenta regresiva del cierre de caja, de 5 a 0, mostrando cada número
    por pantalla y cerrando con la aclaratoria de que cerró caja.
    Recibe: un número entero positivo.
    Devuelve: nada, solo imprime en pantalla.
    """
    if numero == 0:
        print("¡Caja cerrada!")
        return
    print(numero)
    cuenta_regresiva(numero - 1)

def mostrar_menu_principal():
    """Muestra las opciones del menú principal y devuelve la opción
    elegida por el usuario, ya validada.
    Recibe: nada.
    Devuelve: un número entero entre 1 y 3, que representa la opción elegida.
    """
    print("\n===||| KIOSCO EL CAMPUS |||===")
    print("1) Registrar una venta.")
    print("2) Ver resumen del día.")
    print("3) Cerrar caja y salir.")
    opcion = pedir_entero_en_rango("Elija una opción: ", 1, 3)
    return opcion

# PROGRAMA PRINCIPAL
def menu():
    """Punto de entrada del programa: menú principal del kiosco."""
    opcion = 0
    global total_recaudado, cantidad_ventas, venta_mas_alta
    global total_golosinas, total_bebidas, total_almacen, total_libreria
    global cantidad_efectivo, cantidad_debito, cantidad_credito
    while opcion != 3:
        opcion = mostrar_menu_principal()
        if opcion == 1:
            registrar_venta()
        elif opcion == 2:
            mostrar_resumen_dia()
        else:
            confirmar = pedir_confirmacion("¿Confirma el cierre de caja? (S/N): ")
            if confirmar:
                mostrar_resumen_dia()
                cuenta_regresiva(5)
            else:
                opcion = 0 #Como dijo que no, lo volvemos al menú principal.
    print("¡Hasta mañana, Don Ramón! Gracias por utilizar nuestro programa. :)")
menu()