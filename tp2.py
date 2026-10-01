"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico Nro. 2 — Sistema de gestión de ventas: Kiosco "El Campus"

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
RANKING_NOMBRE, RANKING_UNIDADES, RANKING_IMPORTE = 0, 1, 2
TOPE_DE_CODIGO = 9999
TOPE_DE_STOCK = 9999

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

def catalogo_inicial():
    """Devuelve el catálogo de partida del kiosco (lista de listas)."""
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

def mostrar_catalogo(catalogo):
    """Permite ver el catálogo en formato de tabla.
    Recibe: el catálogo (lista de productos).
    Pre: cada producto es una lista [codigo, nombre, categoria, precio, stock].
    Post: imprime un renglón por producto, en el orden en que vienen en la lista.
    No modifica el catálogo ni devuelve nada.
    """
    print("\n****** CATÁLOGO DEL QUIOSCO ******")
    print("Código | Nombre | Categoría | Precio | Stock")
    for i in range(len(catalogo)):
        producto = catalogo[i]
        categoria = CATEGORIAS[producto[CATEGORIA] - 1]
        precio = "$" + formato_de_precio(producto[PRECIO])
        print(f"{producto[CODIGO]},{producto[NOMBRE]},{categoria},{precio},{producto[STOCK]}")

def buscar_por_codigo(catalogo, codigo):
    """Busca un producto por código con BÚSQUEDA BINARIA.
    Pre:  catalogo es una lista de productos ordenada por código (ascendente).
    Post: devuelve la posición del producto con ese código, o -1 si no está.
    No modifica el catálogo.
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

def buscar_por_nombre(catalogo, texto):
    """Busca productos en el catálogo cuyo nombre contiene 'texto' (búsqueda secuencial).
    Pre: texto no está vacío.
    Post: devuelve una lista con los productos del catálogo que coinciden
    (puede ser vacía). No modifica el catálogo.
    """
    producto_coincidente = []
    texto_buscado = texto.lower()
    for i in range(len(catalogo)):
        nombre_producto = catalogo[i][NOMBRE].lower()
        if texto_buscado in nombre_producto:
            producto_coincidente.append(catalogo[i])
    return producto_coincidente

def formato_de_precio(valor):
    """Establece el tipeo de moneda argentina a un número: 2 decimales, punto de
    miles y coma decimal para los centavos.
    Pre:  valor es un número.
    Post: devuelve un string con el valor formateado, sin el signo '$'.
    """
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return texto

def ordenar(lista, campo, descendente):
    """Ordena "lista" (la lista de listas) en el lugar, por selección,
    según el índice de campo indicado y el sentido pedido.
    Pre: que "campo" sea un índice válido para cada elemento de "lista".
    Post: "lista" queda ordenada ascendentemente por lista[i][campo] si
    descendente es False o descendentemente si es True. No devuelve nada.
    """
    for i in range(len(lista) - 1):
        p = buscar_extremo(lista, i, len(lista) - 1, campo, descendente)
        lista[p], lista[i] = lista[i], lista[p]
 
def buscar_extremo(lista, desde, hasta, campo, descendente):
    """Busca la posición del mínimo o máximo en
    lista[desde]..lista[hasta] inclusive; compara por "campo".
    Pre: 0 <= desde <= hasta < len(lista). "campo" es un índice válido
    para cada elemento de "lista".
    Post: devuelve la posición del elemento extremo (mínimo si descendente
    es False, máximo si es True). No modifica "lista".
    """
    extremo = lista[desde][campo]
    p = desde
    for i in range(desde + 1, hasta + 1):
        if descendente:
            if lista[i][campo] > extremo:
                extremo = lista[i][campo]
                p = i
        else:
            if lista[i][campo] < extremo:
                extremo = lista[i][campo]
                p = i
    return p  

def armar_ranking(catalogo, ventas):
    """Elabora una tabla de productos vendidos.
    Pre:  recibe la lista de catálogo y la de ventas realizadas
    Post: devuelve una lista de [nombre, unidades_vendidas, importe_total],
    un elemento por producto con al menos una venta.
    """
    lista_de_ranking = []
    for i in range(len(ventas)):
        venta = ventas[i]
        posicion_producto = buscar_por_codigo(catalogo, venta[CODIGO_VENTA])
        nombre_producto = catalogo[posicion_producto][NOMBRE]
        posicion_en_ranking = buscar_en_ranking(lista_de_ranking, nombre_producto)
        if posicion_en_ranking == -1:
            lista_de_ranking.append([nombre_producto, venta[CANTIDAD], venta[IMPORTE_FINAL]])
        else:
            lista_de_ranking[posicion_en_ranking][RANKING_UNIDADES] += venta[CANTIDAD]
            lista_de_ranking[posicion_en_ranking][RANKING_IMPORTE] += venta[IMPORTE_FINAL]
    return lista_de_ranking

def armar_matriz(catalogo, ventas):
    """Arma los importes vendidos por categoría y medio de pago.
    Recibe el catálogo ordenado por código y el historial de ventas.
    Pre: cada venta corresponde a un producto del catálogo y a un medio de pago válido.
    Post: devuelve una matriz de categorías por medios de pago, sin modificar las listas.
    """
    matriz = []
    for i in range(len(CATEGORIAS)):
        fila = []
        for j in range(len(MEDIOS_PAGO)):
            fila.append(0)
        matriz.append(fila)

    for i in range(len(ventas)):
        venta = ventas[i]
        posicion_producto = buscar_por_codigo(catalogo, venta[CODIGO_VENTA])
        categoria = catalogo[posicion_producto][CATEGORIA]
        fila = categoria - 1
        columna = venta[MEDIO_PAGO] - 1
        matriz[fila][columna] += venta[IMPORTE_FINAL]

    return matriz

def buscar_en_ranking(ranking, nombre):
    """Busca el nombre del producto ingresado entre los productos ya cargados en el ranking.
    Pre:  recibe una lista y un nombre a buscar
    Post: devuelve la posición donde está ese nombre en "ranking"
    o -1 si todavía no se agregó.
    """
    for i in range(len(ranking)):
        if ranking[i][RANKING_NOMBRE] == nombre:
            return i
    return -1

def ranking_ordenado(catalogo, ventas):
    """Confecciona el ranking de productos vendidos y lo ordena por unidades.
    Recibe: el catálogo y la lista de ventas.
    Pre: el catálogo está ordenado por código (ascendente). Asimismo, las ventas
    corresponden a un producto del catálogo.
    Post: devuelve una lista con [nombre, unidades, importe] ordenada de mayor
    a menor por unidades vendidas (estará vacía si no hay ventas).
    """
    ranking = armar_ranking(catalogo, ventas)
    ordenar(ranking, RANKING_UNIDADES, True)
    return ranking

def productos_a_reponer(catalogo):
    """Busca los productos con stock por debajo del mínimo.
    Pre: recibe el catálogo con productos y su stock actual.
    Post: devuelve la lista de productos del catálogo con stock 
    menor a STOCK_MINIMO. Aún no están ordenados.
    """
    mercancia_a_reponer = []
    for i in range(len(catalogo)):
        if catalogo[i][STOCK] < STOCK_MINIMO:
            mercancia_a_reponer.append(catalogo[i])
    return mercancia_a_reponer

def reposicion_ordenada(catalogo):
    """Elabora la lista de productos a reponer ordenada por stock.
    Pre: debe recibir el catálogo.
    Post: devuelve los productos que tengan stock menor a STOCK_MINIMO, ordenados de
    menor a mayor. No modifica el orden del catálogo.
    """
    lista_de_reposicion = productos_a_reponer(catalogo)
    ordenar(lista_de_reposicion, STOCK, False)
    return lista_de_reposicion

def productos_de_categoria(catalogo, categoria):
    """Busca secuencialmente los productos de una categoría.
    Recibe: el catálogo y el número de categoría.
    Pre: categoria es un entero entre 1 y 4.
    Post: devuelve una lista con los productos de esa categoría
    (puede resultar vacía). No modifica el catálogo.
    """
    productos = []
    for i in range(len(catalogo)):
        if catalogo[i][CATEGORIA] == categoria:
            productos.append(catalogo[i])
    return productos

def pedir_texto_no_vacio(mensaje):
    """Pide un texto/nombre y reintenta hasta que tenga al menos un carácter
    que no sea espacio o vacío.
    Recibe: mensaje (str) a mostrar.
    Devuelve: el texto ingresado, sin espacios sobrantes al inicio ni al final.
    """
    texto = input(mensaje).strip()
    while texto == "":
        print("Entrada inválida. No puede estar vacío.")
        texto = input(mensaje).strip()
    return texto

def formatear_nombre(nombre):
    """Deja el texto solo con la primera letra en mayúscula.
    Recibe: nombre (str).
    Pre: nombre no debe estar vacío y no tiene espacios sobrantes.
    Post: devuelve el nombre con su primera letra en mayúscula y el resto
    sin cambios.
    """
    return nombre[0].upper() + nombre[1:]

def agregar_producto(catalogo):
    """Permite ingresar los datos de un producto nuevo, los valida y lo agrega al catálogo.
    Recibe: el catálogo.
    Pre: el catálogo está ordenado por código (ascendente).
    Post: el catálogo tiene un producto más, sin código repetido; además, sigue
    ordenado por código. No devuelve nada.
    """
    codigo = pedir_entero_en_rango("Código del nuevo producto: ", 1, TOPE_DE_CODIGO)
    while buscar_por_codigo(catalogo, codigo) != -1:
        print("Ya existe un producto con ese código. Ingrese otro código diferente.")
        codigo = pedir_entero_en_rango("Código del nuevo producto: ", 1, TOPE_DE_CODIGO)
    nombre = formatear_nombre(pedir_texto_no_vacio("Nombre del producto: "))
    categoria = categoria_producto()
    precio = pedir_real_en_rango("Precio del producto: ", 0)
    stock = pedir_entero_en_rango("Stock inicial: ", 0, TOPE_DE_STOCK)
    catalogo.append([codigo, nombre, categoria, precio, stock])
    ordenar(catalogo, CODIGO, False)
    print(f"¡Producto '{nombre}' agregado exitosamente al catálogo!")

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

def registrar_venta(catalogo, ventas):
    """Registra una venta, actualiza el stock y agrega la tupla al historial.
    Recibe el catálogo ordenado por código y la lista de ventas.
    Pre: el catálogo está ordenado por código y las ventas tienen número correlativo.
    Post: si se confirma una venta, descuenta el stock y agrega su tupla;
    si se ingresa 0 como código, no modifica el catálogo ni las ventas.
    Devuelve: nada.
    """
    while True:
        codigo = pedir_entero_en_rango("Código del producto (0 para cancelar): ", 0, TOPE_DE_CODIGO)
        if codigo == 0:
            print("Registro de venta cancelado.")
            return

        posicion = buscar_por_codigo(catalogo, codigo)
        if posicion == -1:
            print("No existe un producto con ese código. Intente nuevamente.")
            continue

        producto = catalogo[posicion]
        print(f"Producto: {producto[NOMBRE]}")
        print(f"Precio: ${formato_de_precio(producto[PRECIO])}")
        print(f"Stock disponible: {producto[STOCK]}")
        if producto[STOCK] == 0:
            print("El producto no tiene stock disponible.")
            continue
        break

    cantidad_unidades = pedir_entero_en_rango(
        "Cantidad a vender: ", 1, producto[STOCK]
    )
    print("Medio de pago:")
    print("1) Efectivo")
    print("2) Débito")
    print("3) Crédito")
    medio_de_pago = pedir_entero_en_rango("Seleccione una opción: ", 1, 3)

    subtotal = calcular_subtotal(producto[PRECIO], cantidad_unidades)
    descuento_monto = calcular_descuento_por_monto(subtotal)
    ajuste_medio_pago = calcular_ajuste_medio_pago(subtotal, descuento_monto, medio_de_pago)
    importe_final = calcular_importe_final(subtotal, descuento_monto, ajuste_medio_pago)

    numero_venta = len(ventas) + 1
    print("===== TICKET DE VENTA =====")
    print(f"Número de venta: {numero_venta}")
    print(f"Producto: {producto[NOMBRE]}")
    print(f"Cantidad: {cantidad_unidades}")
    print(f"Medio de pago: {nombre_de_medio_de_pago(medio_de_pago)}")
    print(f"Subtotal: ${formato_de_precio(subtotal)}")
    if descuento_monto > 0:
        print(f"Descuento por monto ({PORCENTAJE_DESCUENTO_MONTO}%): -${formato_de_precio(descuento_monto)}")
    if ajuste_medio_pago < 0:
        print(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}%): -${formato_de_precio(abs(ajuste_medio_pago))}")
    elif ajuste_medio_pago > 0:
        print(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}%): +${formato_de_precio(ajuste_medio_pago)}")
    print(f"IMPORTE FINAL: ${formato_de_precio(importe_final)}")
    print("===========================")

    producto[STOCK] -= cantidad_unidades
    ventas.append((numero_venta, codigo, cantidad_unidades, medio_de_pago, importe_final))

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
    Devuelve: un número entero entre 1 y 6, que representa la opción elegida.
    """
    print("\n===||| KIOSCO EL CAMPUS |||===")
    print("1) Registrar una venta.")
    print("2) Consultar el catálogo.")
    print("3) Ver resumen del día.")
    print("4) Ranking de productos más vendidos.")
    print("5) Tabla categoría x medio de pago.")
    print("6) Cerrar caja y salir")

    opcion = pedir_entero_en_rango("Elija una opción: ", 1, 6)
    return opcion

def menu_catalogo(catalogo):
    """Submenú que permite acceder a funciones pertenecientes al catálogo. 
    Se repite hasta elegir la opción 6.
    Recibe: el catálogo.
    Pre: el catálogo está ordenado por código (ascendente).
    Post: el catálogo podría haber adquirido productos nuevos, pero sigue ordenado
    por código. No devuelve nada.
    """
    opcion = 0
    while opcion != 6:
        print("\n<<< CATÁLOGO DEL QUIOSCO >>>")
        print("1) Mostrar inventario completo.")
        print("2) Buscar por código.")
        print("3) Buscar por nombre.")
        print("4) Inventario por categoría.")
        print("5) Agregar un producto para la venta.")
        print("6) Volver al menú principal.")
        opcion = pedir_entero_en_rango("Elija una opción: ", 1, 6)

        if opcion == 1:
            mostrar_catalogo(catalogo)
        elif opcion == 2:
            codigo = pedir_entero_en_rango("Código a buscar: ", 1, TOPE_DE_CODIGO)
            posicion = buscar_por_codigo(catalogo, codigo)
            if posicion == -1:
                print("No existe un producto con ese código.")
            else:
                mostrar_catalogo([catalogo[posicion]])
        elif opcion == 3:
            texto = pedir_texto_no_vacio("¿Qué busca? Ingréselo: ")
            coincidencias = buscar_por_nombre(catalogo, texto)
            if len(coincidencias) == 0:
                print("No hay productos que coincidan con ese texto.")
            else:
                mostrar_catalogo(coincidencias)
        elif opcion == 4:
            categoria = categoria_producto()
            productos = productos_de_categoria(catalogo, categoria)
            if len(productos) == 0:
                print("No hay productos en esa categoría.")
            else:
                mostrar_catalogo(productos)
                cantidad_a_reposicion = len(productos_a_reponer(productos))
                print(f"Productos con stock por debajo del mínimo ({STOCK_MINIMO}): {cantidad_a_reposicion}")
        elif opcion == 5:
            agregar_producto(catalogo)

# PROGRAMA PRINCIPAL
def menu():
    """Punto de entrada del programa: menú principal del kiosco."""
    catalogo = catalogo_inicial()
    ordenar(catalogo, CODIGO, False)
    ventas = []
    opcion = 0
    while opcion != 6:
        opcion = mostrar_menu_principal()
        if opcion == 1:
            registrar_venta(catalogo, ventas)
        elif opcion == 2:
            menu_catalogo(catalogo)
        elif opcion == 3:
            mostrar_resumen_dia(catalogo, ventas)
        elif opcion == 4:
            mostrar_ranking(ranking_ordenado(catalogo, ventas))
        elif opcion == 5:
            mostrar_matriz(armar_matriz(catalogo, ventas))        
        else:
            confirmar = pedir_confirmacion("¿Confirma el cierre de caja? (S/N): ")
            if confirmar:
                mostrar_resumen_dia(catalogo, ventas)
                mostrar_ranking(ranking_ordenado(catalogo, ventas))
                mostrar_reposicion(reposicion_ordenada(catalogo))
                cuenta_regresiva(5)
            else:
                opcion = 0 #Como dijo que no, lo volvemos al menú principal.
    print("¡Hasta mañana, Don Ramón! Gracias por utilizar nuestro programa. :)")
menu()