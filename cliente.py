import requests
import json
import os
import io


# Función para mostrar los resultados
# de una forma agradable para el usuario
def mostrar_resultado(resp, modoJ : bool):
    if modoJ:
        print(resp.text)
    else:
        dicts = resp.json()
        i = 1
        for libro in dicts:
            print("Libro n°: " + str(i))
            print("Titulo: " + libro["title"] + \
                " | Año: " + str(libro["year"]) + \
                " | Autor: " + libro["author"])
            print("País de Origen: " + libro["country"] + \
                " | Idioma: " + libro["language"] + \
                " | N° de Páginas: " + str(libro["pages"]))
            print("Link: " + libro["link"].strip())
            print("Link de imagen: " + libro["imageLink"])
            
            i += 1
        if i == 1:
            print("No hubieron resultados")

ip = input("Ingrese la IP del servidor (predeterminado = 127.0.0.1): ")
if ip == "": ip = "127.0.0.1"
puerto = input("Ingrese el puerto del servidor (predeterminado = 8000): ")
if puerto == "": puerto = "8000"
dir = "http://" + ip + ":" + puerto

salir = False
modoJson = False

while salir == False:
    print("Acción:")
    print("      1. Obtener libros")
    print("      2. Agregar libros")
    print("      3. Eliminar libro")
    print("      4. Actualizar un libro existente")
    print("      5. Obtener books.json")
    print("      6. Eliminar books.json")
    print("      7. Obtener resumen de la db")
    print("      8. Cambiar modo de visualización de datos")
    print("      9. Salir")
    llamada = input("Seleccione una acción: ")    

    match llamada:
        case "1":
            print("Criterio de búsqueda:")
            print("      1. Título")
            print("      2. Autor")
            print("      3. Año")
            print("      4. País de Origen")
            print("      5. Idioma")
            print("      6. Páginas")
            print("      7. Búsqueda avanzada")
            print("      8. Cancelar")
            llamada = input("Seleccione un criterio: ")
            match llamada:
                case "1":
                    llamada = input("Ingrese el nombre: ")
                    resp = requests.get(dir + "/get-book?title=" + llamada)
                    mostrar_resultado(resp, modoJson)
                case "2":
                    llamada = input("Ingrese el autor: ")
                    resp = requests.get(dir + "/get-book?author=" + llamada)
                    mostrar_resultado(resp, modoJson)
                case "3":
                    params = "?"
                    print("Deje en blanco para no filtrar:")
                    minYear = input("Ingrese el año mínimo: ")
                    if minYear != "":
                        params += "minYear=" + minYear
                    maxYear = input("Ingrese el año máximo: ")
                    if maxYear != "":
                        params += "maxYear=" + maxYear
                    resp = requests.get(dir + "/get-book" + params)
                    mostrar_resultado(resp, modoJson)
                case "4":
                    llamada = input("Ingrese el país de origen: ")
                    resp = requests.get(dir + "/get-book?country=" + llamada)
                    mostrar_resultado(resp, modoJson)
                case "5":
                    llamada = input("Ingrese el idioma: ")
                    resp = requests.get(dir + "/get-book?language=" + llamada)
                    mostrar_resultado(resp, modoJson)
                case "6":
                    params = "?"
                    print("Deje en blanco para no filtrar:")
                    minPages = input("Ingrese la cantidad mínima de páginas: ")
                    if minPages != "":
                        params += "minPages=" + minPages
                    maxPages = input("Ingrese la cantidad máxima de páginas: ")
                    if maxPages != "":
                        params += "maxPages=" + maxPages
                    resp = requests.get(dir + "/get-book" + params)
                    mostrar_resultado(resp, modoJson)
                case "7":
                    params = "?"
                    print("A continuación, inserte los filtros de búsqueda deseados.\n\
                           Deje en blanco para ignorar el filtro.")
                    titulo = input("Título: ")
                    if titulo != "": params += "&title=" + titulo
                    autor = input("Autor: ")
                    if autor != "": params += "&author=" + autor
                    minAno = input("Escrito después del año: ")
                    if minAno != "": params += "&minYear=" + minAno
                    maxAno = input("Escrito antes del año: ")
                    if maxAno != "": params += "&maxYear=" + maxAno
                    pais = input("País de Origen: ")
                    if pais != "": params += "&country=" + pais
                    idioma = input("Idioma: ")
                    if idioma != "": params += "&language=" + idioma
                    minPaginas = input("Mínimo de páginas: ")
                    if minPaginas != "": params += "&minPages=" + minPaginas
                    maxPaginas = input("Máximo de páginas: ")
                    if maxPaginas != "": params += "&maxPages=" + maxPaginas
                    resp = requests.get(dir + "/get-book" + params)
                    mostrar_resultado(resp, modoJson)
                case "8":
                    continue
                case _: 
                    print("Opción inválida.")
                    continue
        case "2":
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = input("Año: ")
            pais = input("País de Origen: ")
            idioma = input("Idioma: ")
            paginas = input("Páginas: ")

            params = "?title=" + titulo + "&author=" + autor + "&year=" + \
                     ano + "&country=" + pais + "&language=" + idioma + "&pages=" + paginas
            
            link = input("Link (Deje en blanco si no posee uno): ")
            if link != "": 
                params += "&link=" + link
            imageLink = input("Link de Imagen (Deje en blanco si no posee uno): ")
            if imageLink != "": 
                print("Hola")
                params += "&imageLink=" + imageLink
            
            resp = requests.post(dir + "/add-book" + params)
            if resp.text == "null" and modoJson == False:
                print("Libro creado exitosamente.")
            elif resp.text != "null":
                print("Ha ocurrido un error.")
            else: print(resp.text)
        case "3":
            llamada = input("Nombre del libro que desea eliminar: ")
            resp = requests.delete(dir + "/delete?title=" + llamada)
            if resp.text == "null" and modoJson == False:
                print("Libro eliminado exitosamente.")
            elif resp.text != "null":
                print("Ha ocurrido un error.")
            else: print(resp.text)
        case "4":
            title = input("Nombre del libro a editar: ")
            resp = requests.get(dir + "/get-book?title=" + title)
            
            dicts = resp.json()
            if dicts != []:
                libro = dicts[0]
                print("Titulo: " + libro["title"] + \
                    " | Año: " + str(libro["year"]) + \
                    " | Autor: " + libro["author"])
                print("País de Origen: " + libro["country"] + \
                    " | Idioma: " + libro["language"] + \
                    " | N° de Páginas: " + str(libro["pages"]))
                print("Link: " + libro["link"].strip())
                print("Link de imagen: " + libro["imageLink"])
            else:
                print("No se encontró el libro.")
                continue
            
            print("Deje en blanco para no modificar un parámetro.")

            params = "?title=" + title
            nuevoTitulo = input("Nuevo título: ")
            if nuevoTitulo != "": params += "&newTitle=" + nuevoTitulo
            autor = input("Autor: ")
            if autor != "": params += "&author=" + autor
            ano = input("Año: ")
            if ano != "": params += "&year=" + ano
            pais = input("País de Origen: ")
            if pais != "": params += "&country=" + pais
            idioma = input("Idioma: ")
            if idioma != "": params += "&language=" + idioma
            paginas = input("Páginas: ")
            if paginas != "": params += "&pages=" + paginas

            print("Para los links, escriba \"-\" si desea eliminar el parámetro")
            link = input("Link: ")
            if link != "": params += "&link=" + link
            imageLink = input("Link de Imágen: ")
            if imageLink != "": params += "&imageLink=" + imageLink

            resp = requests.put(dir + "/update" + params)
            if resp.text == "null" and modoJson == False:
                print("Libro editado exitosamente.")
            elif resp.text != "null":
                print("Ha ocurrido un error.")
            else: print(resp.text)
        case "5":
            print("Descargando...")
            with open("books.json", "w") as file:
                data = requests.get(dir + "/db")
                dataJson = data.json()
                json.dump(dataJson, file)
        case "6":
            os.remove("books.json")   
        case "7":
            resp = requests.get(dir + "/summary")
            if modoJson:
                print(resp.text)
            else: 
                summary = resp.json()
                print("Cantidad de libros:", summary["cantidad"])
                print("Propiedades de los libros: ")
                for propiedad, tipo in summary["campos"].items(): 
                    print("Propiedad: " + propiedad + ",\t tipo: " + tipo)
        case "8":
            print("Existen dos modos de visualización.")
            print("Modo usuario: Visualización cómoda e intuitiva.")
            print("Modo Json: Los datos serán devueltos sin procesar, en formato Json.")
            if modoJson:
                modo = "modo Json"
            else:
                modo = "modo usuario"
            print("El modo actual es: " + modo)
            cambio = input("Desea cambiar de modo?(y|Y/n|N): ")
            if cambio == "y" or cambio == "Y":
                modoJson = not modoJson
        case "9": 
            print("Cerrando...")
            salir = True
        case _: print("Opción inválida.")
    input("Presione Enter para continuar.")
