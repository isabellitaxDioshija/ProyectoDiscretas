from sys import stdin

v = dict() # Diccionario para almacenar los valores de verdad

def str_to_list(s: str, ignore: set) -> list[str]: #función para convertir una cadena de texto en una lista de caracteres ignorando los espacios en blanco que están en ignore
    lista = [] #lista vacia para guardar los caracteres
    for caracter in s: #bucle para recorrer cada caracter de la cadena de texto
        if caracter not in ignore: 
            lista.append(caracter)#se agregan los caracteres (sin contar los del ignore) a la lista vacía
    return lista
     #se retorna la lista con con los caracteres agregados

def V(form: list, r: int, l: int): #funcion para valorar las formulas
    if r == l: #si r y l son iguales, entonces sólo hay un caracter
        return v[form[r]] #se retorna el valor de verdad del caracter almacenado en v
        
        

    if form[r] == '!': #condición por si el primer caracter es !: se niega la fórmula
        return not V(form, r + 1, l) #se retorna la fórmula negada 

    if form[r] == '(' and form[l] == ')': #condición para ver si la fórmula está entre paréntesis
        cnt = 0 #contador para la cantidad de paréntesis abiertos y cerrados
        md = -1 #indice del operador principal (& o |) fuera de paréntesis, inicializado en -1
        for i in range(r + 1, l): #Recorremos toda la expresión desde r + 1 hasta l - 1
            if form[i] == '(':
                cnt += 1 #aumentar contador
            elif form[i] == ')':
                cnt -= 1 #restar al contador
            if form[i] in {'&', '|'} and cnt == 0: #en caso de que se encuentre & o | y el contador esté en cero, es decir, estamos fuera de paréntesis, ese es el operador principal
                md = i #se guarda la posición del operador

        if md != -1: #condición por si se encuentra un operador principal
            izq = V(form, r + 1, md - 1) #se evalúa lo que está antes del operador principal
            der = V(form, md + 1, l - 1) #se evalúa lo que está después del op. principal

            if form[md] == '&': #condición en caso de que el op. principal sea un & o and
                return izq and der #se retorna ambas partes de la fórmula sometidas a un operador AND
            elif form[md] == '|': #condición para cuando el op. principal sea un | o or
                return izq or der # se retorna ambas partes de la fórmula sometidas a un operador OR

    return -1  #si la expresión no se reconoce, se toma como inválida.

def probarCombinaciones(atomos, valores, i, resultados, form): #función para probar todos los valores de verdad posibles para la fórmula, parte b.
    if i == len(atomos): #si i llega al tamaño de la lista atomos, significa que ya asignamos valores a todos los átomos
        for j in range(len(atomos)): #bucle para recorrer la lista de átomos y les asigna su valor actual en v
            v[atomos[j]] = valores[j] #asignamos el valor de verdad al átomo en el diccionario v
        
        resultados.add(V(form, 0, len(form) - 1)) #se evalúa la expresión con la funcion V() y se guarda en resultados
        return 
  
    valores[i] = False #primero se intenta con el átomo con valor falso (0) 
    probarCombinaciones(atomos, valores, i + 1, resultados, form) 

    valores[i] = True #luego, se intenta con el átomo con valor verdadero (1)
    probarCombinaciones(atomos, valores, i + 1, resultados, form)

def analizarFormula(form): #función para determinar si una fórmula es una tautología, una contingencia o una contradiccón
    atomos = sorted(set(c for c in form if c.isalpha()))  #obtenemos los átomos únicos
    resultados = set()  #en este set se guardan los resultados de la evaluación

    probarCombinaciones(atomos, [False] * len(atomos), 0, resultados, form) #generamos todas las combinaciones posibles y las evaluamos

    if resultados == {True}: #si en todas la pruebas da verdadero o 1, entonces se retorna 1, ya que es una tautología
        return 1 
    elif resultados == {False}: #si en todas las pruebas da falso o 0, entonces se retorna 0, ya que es una contradicción
        return 0  
    else:
        return -1 #este else es en caso de que en algunas pruebas salga falso y en otras verdadero, se retorna -1, ya que es una contingencia

def main(): #función preincipal 
    print("Seleccione una opción: ")
    print("1. Valorar fórmula(verdadero o falso) 2. Probar fórmulas(tautología, contradicción o contingencia)")

    opcion = int(input()) #lee la opción elegida y la convierte a entero

    if opcion == 1: #parte a: Función de valoración
        N = int(stdin.readline().strip()) # se lee el número de átomos que se van a ingresar
        for i in range(N): 
            var, value = stdin.readline().split() #se lee el nombre del átomo y su valor de verdad (1 o 0)
            v[var] = bool(int(value)) #se convierte el valor a bool y se guarda en el diccionario v
        
        M = int(stdin.readline().strip()) #lee el numero de fórmulas que se van a valorar 
        for i in range(M):
            form = str_to_list(stdin.readline().strip(), {' '}) #convierte la fórmula en una lista sin espacios 
            ans = V(form, 0, len(form) - 1) #se evalúa la fórmula lógica con la función V()
            if ans:
                print("1")  #si la expresión es verdadera, se imprime 1
            else:
                print("0")  #si la expresión es falsa, se imprime 0


    elif opcion == 2: #parte b: Probador de fórmulas
        S = int(stdin.readline().strip()) #se leen el número de fórmulas que se van a probar, eliminando los espacios y se convierte la entrada a un entreo
        for i in range(S): #bucle para analizar cada una de las formulas que se ingresen
            form = str_to_list(stdin.readline().strip(), {' '}) #se convierte la fórmula en una lista sin espacios
            print(analizarFormula(form)) #llamamos la función analizar_formula(form) y se imprime el resultado (1 si es tautología, 0 si es contradicción o -1 si es contingencia)

main() #llamamos a la función main para ejecutar el programa
