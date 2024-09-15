#Alejandra Rodriguez Guevara 21310127 7E1

import sqlite3

# Crear o conectar una base de datos SQLite
conn = sqlite3.connect('SistemasMecatronicos.db')
cursor = conn.cursor()

# Crear tabla de preguntas y respuestas si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    answer TEXT
                )''')

# Crear tabla para almacenar información sobre tecnologías
cursor.execute('''CREATE TABLE IF NOT EXISTS tecnologias (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    funcion TEXT,
                    funcionamiento TEXT,
                    costo REAL
                )''')

# Datos precargados
precargadas = [
    ("Hola", "Hola! ¿Cómo estás?"),
    ("¿Cómo estás?", "Estoy bien, gracias por preguntar. ¿De qué te gustaría hablar? ¿Tienes alguna tecnología en mente? Dime el nombre de la tecnología"),
    ("Quiero hablar de algo", "¿De qué te gustaría hablar? ¿Tienes alguna tecnología en mente? Dime el nombre de la tecnología")
]


# Insertar las preguntas precargadas solo si no existen en la base de datos
for pregunta, respuesta in precargadas:
    cursor.execute('SELECT * FROM knowledge_base WHERE question=?', (pregunta,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO knowledge_base (question, answer) VALUES (?, ?)', (pregunta, respuesta))

conn.commit()

def buscar_respuesta(pregunta):
    cursor.execute('SELECT answer FROM knowledge_base WHERE question=?', (pregunta,))
    respuesta = cursor.fetchone()
    if respuesta:
        return respuesta[0]
    else:
        return None

def agregar_conocimiento(pregunta, respuesta):
    cursor.execute('INSERT INTO knowledge_base (question, answer) VALUES (?, ?)', (pregunta, respuesta))
    conn.commit()

def agregar_tecnologia(nombre, funcion, funcionamiento, costo):
    cursor.execute('INSERT INTO tecnologias (nombre, funcion, funcionamiento, costo) VALUES (?, ?, ?, ?)',
                   (nombre, funcion, funcionamiento, costo))
    conn.commit()

def buscar_tecnologia(nombre):
    cursor.execute('SELECT * FROM tecnologias WHERE nombre=?', (nombre,))
    tecnologia = cursor.fetchone()
    if tecnologia:
        return {
            'id': tecnologia[0],
            'nombre': tecnologia[1],
            'funcion': tecnologia[2],
            'funcionamiento': tecnologia[3],
            'costo': tecnologia[4]
        }
    else:
        return None

# Nueva función para editar la información de la tecnología
def editar_tecnologia(id_tecnologia, campo, nuevo_valor):
    if campo == "nombre":
        cursor.execute('UPDATE tecnologias SET nombre=? WHERE id=?', (nuevo_valor, id_tecnologia))
    elif campo == "funcion":
        cursor.execute('UPDATE tecnologias SET funcion=? WHERE id=?', (nuevo_valor, id_tecnologia))
    elif campo == "funcionamiento":
        cursor.execute('UPDATE tecnologias SET funcionamiento=? WHERE id=?', (nuevo_valor, id_tecnologia))
    elif campo == "costo":
        cursor.execute('UPDATE tecnologias SET costo=? WHERE id=?', (float(nuevo_valor), id_tecnologia))
    conn.commit()

# Chat sencillo con opción de salir
print("Chatbot: ¡Hola! Si en algún momento quieres salir del chat, escribe 'salir'.")
print("Chatbot: Para añadir o consultar alguna tecnologia a la base de datos escribe : ´Quiero hablar de algo´ en el chat.")
print("Chatbot: En caso de querer seguir una conversacion solo preguntame cosas, si no lo se ayudame a añardirlo a la base de datos para futuras conversaciones")

while True:
    user_input = input("Tú: ")
    
    # Condición para salir del chat
    if user_input.lower() == "salir":
        print("Chatbot: ¡Adiós! Gracias por conversar conmigo.")
        break

    respuesta = buscar_respuesta(user_input)
    
    if respuesta:
        print(f"Chatbot: {respuesta}")
        if "¿Tienes alguna en mente?" in respuesta:
            nombre_tecnologia = input("Tú: ")
            tecnologia = buscar_tecnologia(nombre_tecnologia)
            if tecnologia:
                print(f"Chatbot: La tecnología '{tecnologia['nombre']}' tiene la siguiente información almacenada:")
                print(f"  Función: {tecnologia['funcion']}")
                print(f"  Funcionamiento: {tecnologia['funcionamiento']}")
                print(f"  Costo aproximado: ${tecnologia['costo']}")
                
                # Preguntar si el usuario desea editar la información
                editar = input("Chatbot: ¿Te gustaría editar alguna información sobre esta tecnología? (sí/no) ").lower()
                if editar == "sí":
                    campo = input("Chatbot: ¿Qué te gustaría editar? (nombre/funcion/funcionamiento/costo) ").lower()
                    nuevo_valor = input(f"Chatbot: Ingresa el nuevo valor para {campo}: ")
                    editar_tecnologia(tecnologia['id'], campo, nuevo_valor)
                    print(f"Chatbot: La tecnología '{nombre_tecnologia}' ha sido actualizada.")
            else:
                print("Chatbot: No tengo información sobre esa tecnología. Vamos a recopilarla.")
                funcion = input("Chatbot: ¿Cuál es la función o aplicación de esta tecnología? ")
                funcionamiento = input("Chatbot: ¿Cómo funciona esta tecnología? ")
                costo = input("Chatbot: ¿Cuál es el costo aproximado de esta tecnología? ")
                agregar_tecnologia(nombre_tecnologia, funcion, funcionamiento, costo)
                print("Chatbot: Gracias, he almacenado la información de esta tecnología.")
    else:
        print("Chatbot: No tengo una respuesta para eso. ¿Cuál debería ser la respuesta?")
        nueva_respuesta = input("Ingresa la nueva respuesta: ")
        agregar_conocimiento(user_input, nueva_respuesta)
        print("Chatbot: Gracias, he aprendido algo nuevo!")