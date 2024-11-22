import tkinter as tk #Crea interfaces
from tkinter import messagebox #Muestra cuadros de dialogo
import nltk #Es para la gramatica, arboles 
from nltk import CFG, ChartParser, Tree #FDefine una gramatica, analiza la expresion basada en la gramatica, crea arboles
from nltk.tree import ParentedTree #Crea arboles

tipo_arbol = "normal" #Variable global para saber que tipo de arbol se va a mostrar

def obtener_pasos_derivacion(tree): #Función para obtener los pasos de derivación del árbol sintáctico

    pasos = [] #Lista para guardar los pasos de derivación
    
    def recorrer_arbol(node, expresion_actual): #Función para recorrer el árbol sintáctico
        if len(node) == 1 and isinstance(node[0], str): #Si el nodo es terminal se regresa(no tiene hijos)
            return
            
        produccion = f"{node.label()} ->" #Obtiene el nombre del nodo actual
        for child in node: #Recorre los hijos del nodo
            if isinstance(child, Tree): #verifica si el hijo es un nodo no terminal o terminal
                produccion += f" {child.label()}" #Si es un nodo no terminal se agrega el nombre del nodo
            else:
                produccion += f" {child}" #Si es un nodo terminal se agrega el valor del nodo
                
        nueva_expresion = [] #Lista para guardar la expresión actual
        for elemento in expresion_actual: #Recorre la expresión actual
            if isinstance(elemento, Tree): #Verifica si el elemento es un nodo no terminal o terminal
                if len(elemento) == 1 and isinstance(elemento[0], str): #Si es un nodo terminal se agrega el valor del nodo 
                    nueva_expresion.append(elemento[0]) #Se agrega el valor del nodo
                else:
                    nueva_expresion.append(elemento.label()) #Si es un nodo no terminal se agrega el nombre del nodo
            else:
                nueva_expresion.append(elemento) #Si es un nodo terminal se agrega el valor del nodo
                
        # Agregar el paso a la lista
        pasos.append(f"{' '.join(nueva_expresion)} \t[{produccion}]") 
        
        for i, child in enumerate(node): #Recorre los hijos del nodo
            if isinstance(child, Tree): #Verifica si el hijo es un nodo no terminal o terminal
                nueva_expr = expresion_actual.copy() #Copia la expresión actual
                nueva_expr[expresion_actual.index(node)] = child #Reemplaza el nodo actual por el hijo
                recorrer_arbol(child, nueva_expr) #Recorre el árbol con el hijo actual
    
    # Iniciar el recorrido desde la raíz
    recorrer_arbol(tree, [tree]) #Llama a la función recorrer_arbol con el árbol y la raíz con el fin de obtener los pasos de derivación
    return pasos #Regresa los pasos de derivación

def analizar_expresion():
    opcion = derivacion_var.get() #Obtiene la opción seleccionada por el usuario

    # Definir la gramática basada en la elección del usuario
    if opcion == "Izquierda":
        gramatica = CFG.fromstring("""
            E -> E '+' T | E '-' T | T
            T -> T '*' F | T '/' F | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'""")
    elif opcion == "Derecha":
        gramatica = CFG.fromstring("""
            E -> T '+' E | T '-' E | T
            T -> F '*' T | F '/' T | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'""")
    else:
        messagebox.showerror("Opción inválida", "La opción seleccionada no es válida. Se usará derivación por izquierda.")
        gramatica = CFG.fromstring("""
            E -> E '+' T | E '-' T | T
            T -> T '*' F | T '/' F | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'""")

    # Obtener la expresión del campo de texto
    entrada_usuario = entrada_text.get()

    # Dividir la entrada por espacios
    expresion_objetivo = entrada_usuario.split()

    # Crear el parser(el que se encarga de analizar la expresión)
    parser = ChartParser(gramatica) 
 
    try:
        for tree in parser.parse(expresion_objetivo): #Recorre los árboles generados por el parser
            resultado_text.delete(1.0, tk.END) #Borra el contenido del campo de texto para mostrar el resultado
            
            # Mostrar los pasos de derivación
            resultado_text.insert(tk.END, f"Pasos de derivación ({opcion}):\n")
            resultado_text.insert(tk.END, "-" * 50 + "\n") 
            pasos = obtener_pasos_derivacion(tree)
            for i, paso in enumerate(pasos, 1):
                resultado_text.insert(tk.END, f"Paso {i}: {paso}\n")
            resultado_text.insert(tk.END, "-" * 50 + "\n\n")

            if tipo_arbol == "normal":
                # Mostrar el árbol normal
                resultado_text.insert(tk.END, "Árbol de derivación normal:\n")
                tree.pretty_print()  # Muestra el árbol en la consola
                tree.draw()  # Abre una ventana con el árbol sintáctico
            if tipo_arbol == "ATS":
                # Crear un árbol ATS
                resultado_text.insert(tk.END, "\nÁrbol ATS simplificado:\n")
                ats_arbol = arbol_ats_crear(tree) #Crea el árbol ATS
                ats_arbol.pretty_print() #Muestra el árbol en la consola
                ats_arbol.draw() #Abre una ventana con el árbol ATS
    except ValueError: #Si la expresión no es válida
        messagebox.showerror("Error de sintaxis", "La expresión no es válida según la gramática.")

def elegir_arbol_normalito(): #Función para elegir el tipo de árbol a mostrar
    global tipo_arbol #Variable global para saber que tipo de árbol se va a mostrar
    tipo_arbol = "normal" #Se elige el árbol normal

def elegir_arbol_ats(): #Función para elegir el tipo de árbol a mostrar
    global tipo_arbol #Variable global para saber que tipo de árbol se va a mostrar
    tipo_arbol = "ATS" #Se elige el árbol ATS

def arbol_ats_crear(tree): #Función para crear el árbol ATS
    def simplificar_arbolito(node): #Función para simplificar el árbol
        if isinstance(node, str): #Si el nodo es una cadena
            return node #Se regresa la cadena
         
        if len(node) == 3 and isinstance(node[1], str) and node[1] in ["+","-","*","/"]: #Si el nodo tiene 3 hijos y el hijo del medio es un operador
            operador = node[1] #Se obtiene el operador
            izquierda = simplificar_arbolito(node[0]) #Se simplifica el hijo izquierdo
            derecha = simplificar_arbolito(node[2]) #Se simplifica el hijo derecho

            if isinstance(izquierda,(Tree, ParentedTree)): #Si el hijo izquierdo es un nodo no terminal
                izquierda_valor = izquierda #Se guarda el nodo izquierdo
            else: #Si el hijo izquierdo es un nodo terminal
                izquierda_valor = Tree(izquierda, []) #Se crea un nodo con el valor del hijo izquierdo

            if isinstance(derecha,(Tree, ParentedTree)): #Si el hijo derecho es un nodo no terminal
                derecha_valor = derecha #Se guarda el nodo derecho
            else: #Si el hijo derecho es un nodo terminal
                derecha_valor = Tree(derecha, []) #Se crea un nodo con el valor del hijo derecho
            return Tree(operador, [izquierda_valor, derecha_valor]) #Se regresa un nodo con el operador y los hijos izquierdo y derecho
        
        elif len(node) == 3 and isinstance(node[0], str) and node[0] == "(" and node[2] == ")": #Si el nodo tiene 3 hijos y el primer y último hijo son paréntesis
            return simplificar_arbolito(node[1]) #Se simplifica el hijo del medio
        
        elif len(node) == 1 and isinstance(node[0], str): #Si el nodo tiene un solo hijo y es una cadena
            return Tree(node[0], []) #Se regresa un nodo con el valor del hijo
        
        for i in range(len(node)): #Recorre los hijos del nodo
            resultado = simplificar_arbolito(node[i]) #Simplifica el hijo actual
            if resultado is not None: #Si el resultado no es nulo
                return resultado #Se regresa el resultado
        return None #Si no se cumple ninguna condición se regresa nulo
    
    arbol_simplificado = tree.copy(deep=True) #Copia el árbol
    resultado = simplificar_arbolito(arbol_simplificado) #Simplifica el árbol
    return resultado if resultado else Tree("Error", []) #Regresa el árbol simplificado

# Crear la ventana principal 
arbolito = tk.Tk()
arbolito.title("Analizador de Expresiones")

entrada_label = tk.Label(arbolito, text="Introduce la expresión a analizar por fi:")
entrada_label.pack(pady=10)

entrada_text = tk.Entry(arbolito, width=50)
entrada_text.pack(pady=5)

derivacion_var = tk.StringVar(value="Izquierda")

derivacion_label = tk.Label(arbolito, text="Elige el tipo de derivación:")
derivacion_label.pack(pady=10)

derivacion_izquierda_radio = tk.Radiobutton(arbolito, text="Izquierda", variable=derivacion_var, value="Izquierda")
derivacion_izquierda_radio.pack()

derivacion_derecha_radio = tk.Radiobutton(arbolito, text="Derecha", variable=derivacion_var, value="Derecha")
derivacion_derecha_radio.pack()

arbol_normal_boton = tk.Button(arbolito, text="Árbol normal", command=elegir_arbol_normalito)
arbol_normal_boton.pack(pady=5)

arbol_ats_boton = tk.Button(arbolito, text="Árbol ATS", command=elegir_arbol_ats)
arbol_ats_boton.pack(pady=5)

analizar_boton = tk.Button(arbolito, text="Analizar", command=analizar_expresion)
analizar_boton.pack(pady=20)

resultado_text = tk.Text(arbolito, width=60, height=15)
resultado_text.pack(pady=10)

arbolito.mainloop()
