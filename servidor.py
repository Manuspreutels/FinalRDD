from fastapi import FastAPI
import requests
import json
import sys

# Dirección de la base de datos
url = "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/books.json"

# uvicorn --reload api:app
# Descargar el archivo JSON
respuesta = requests.get(url)
# print(respuesta.text) para ver el texto crudo
# Convertimos los datos en formato de texto plano a listas y diccionarios (json)
libros = respuesta.json()

# Escribimos el contenido de datos en "books.json"
with open("data/books.json", "w") as archivo_json:
    json.dump(libros, archivo_json)

app = FastAPI()

@app.get("/summary")
def summary():
    num_objetos = len(libros)  # Número de objetos en el archivo
    resumen = dict()
    primer_objeto = libros[0]  # Obtener el primer objeto para analizar sus propiedades
    resumen["cantidad"] = num_objetos
    if num_objetos > 0 :
        resumen["campos"] = dict()
        campos = list(primer_objeto.keys())  # Obtener las campos del primer objeto
        tipos_de_dato = {prop: type(primer_objeto[prop]) for prop in campos}  # Obtener el tipo de dato de cada propiedad
        
        for campo in campos:
            tipo = tipos_de_dato[campo].__name__
            resumen["campos"][campo] = tipo
    else:
        resumen["campos"] = "None"
    return resumen

@app.get("/get-book")
def buscar_libro(title : str = None, author : str = None, 
                 minYear : int = None, maxYear : int = None,
                 minPages : int = None, maxPages : int = None,
                 country : str = None, language : str = None):
    props = [title, author, country, language]
    campos = ["title", "author", "country", "language"]
    templibros = libros # aplicamos los filtros acumulativamente sobre templibros
    biblioteca = []
    
    # Si no se especifican los años mínimos y máximos, serán -inf e inf
    if minYear == None:
        minYear = -sys.maxsize-1
    if maxYear == None:
        maxYear = sys.maxsize
    for libro in templibros:
        if libro["year"] >= minYear and libro["year"] <=  maxYear:
            biblioteca.append(libro)
    templibros = biblioteca
    biblioteca = []

    #lo mismo ocurrirá con las páginas
    if minPages == None:
        minPages = 0
    if maxPages == None:
        maxPages = sys.maxsize
    for libro in templibros:
        if libro["pages"] >= minPages and libro["pages"] <=  maxPages:
            biblioteca.append(libro)
    templibros = biblioteca  # Nos quedamos solo con los elementos de templibros
                             # que cumplan la propiedad
    biblioteca = []
    
    for i in range(0,4):
        if props[i] != None:
            for libro in templibros:
                if libro[campos[i]] == props[i]:
                    biblioteca.append(libro)
            templibros = biblioteca # Nos quedamos solo con los elementos de templibros
                                    # que cumplan la propiedad
            biblioteca = []
    return templibros   # Devolvemos todos los libros que cumplan la propiedad

@app.get("/db")
def devolver_db():
    return libros

@app.post("/add-book")
def crear_libro(title: str, author: str, year: int,
                country: str, pages: int, language: str,                  
                link: str = None, imageLink: str = None):
    libro = dict()
    libro["title"] = title
    libro["author"] = author
    libro["country"] = country
    libro["year"] = year
    # Permitimos la opción de dejar en blanco estos campos
    if link != None:
        libro["link"] = link
    else: libro["link"] = ""
    if imageLink != None:
        libro["imageLink"] = imageLink
    else: libro["imageLink"] = ""

    libro["pages"] = pages
    libro["language"] = language
    libros.append(libro)
    return None

@app.put("/update")
def actualizar_libro(title: str, newTitle: str = None, author: str = None, year: int = None,
                     country: str = None, pages: int = None, language: str = None,
                     link: str = None, imageLink: str = None):
    
    for libro in libros:
        if libro["title"] == title: # encontramos el libro a modificar
            # Se cambian los valores por los deseados, siempre que se especifiquen
            if newTitle != None:
                libro["title"] = newTitle
            if author != None:
                libro["author"] = author
            if year != None:
                libro["year"] = year
            if country != None:
                libro["country"] = country
            if pages != None:
                libro["pages"] = pages
            if language != None:
                libro["language"] = language
            if link != None:
                if link == "-":
                    libro["link"] = ""
                else:
                    libro["link"] = link
            if imageLink != None:
                if imageLink == "-":
                    libro["imageLink"] = ""
                else:
                    libro["imageLink"] = imageLink
    return None  

@app.delete("/delete")
def eliminar_libro(title: str):
    i = 0
    for libro in libros:
        if libro["title"] == title: #encontramos el libro
            libros.pop(i)
            return "Libro eliminado."
        i += 1
    return "Libro no encontrado."
