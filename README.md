# Laboratorio2Web
-   Asignatura: OII436-1
-   Integrantes: Diego Alvarez, Ariel Carrasco, Gabriel Reyes
-   Url del repositorio: https://github.com/Churrascooo/Laboratorio2Web.git
-   Pasos de creacion/activacion entorno virtual:
    1. Desde la terminal: cd C: \Users\Estudiante\Desktop\laboratorio2
    2. Crear entorno virtual: py -m venv .venv
    3. Activarlo en Windows CMD: .venv\Scripts\activate.bat
    4. Instalar dependencias: python -m pip install --upgrade pip
                              python -m pip install -r requirements.txt
    5. Orden de ejecución:
    5.1 python scraper.py
    5.2 python procesamiento.py
    5.3 python buscador.py


## 1. Extracción mediante Web Scraping

### Pregunta 1: ¿Para qué sirve BeautifulSoup y cómo se diferencia de requests?

BeautifulSoup es una biblioteca de Python la cual sirve para analizar (hacer parsing) documentos HTML y XML, permitiendo buscar, navegar y extraer datos específicos de su estructura de forma sencilla, Mientras que Requests es una biblioteca de Python que sirve para enviar solicitudes HTTP a servidores web (como hacer un GET o POST) y descargar el contenido de una página, diferenciandose de esta menra a la primera bibloteca

### Pregunta 2: ¿Qué riesgo existe al depender de selectores HTML específicos si el sitio cambia?

El principal riesgo es que el código de extracción (scraper) se vuelve frágil y dejará de funcionar si los administradores del sitio web realizan actualizaciones en el diseño o en la estructura de la página.

Si el sitio web cambia los nombres de las clases (class), los identificadores (id), o la jerarquía de las etiquetas HTML (por ejemplo, envolviendo el precio en un nuevo div) , los selectores en BeautifulSoup ya no encontrarán ninguna coincidencia. 
Las principales concencuencias serian las siguientes:
 
 - La extracción fallará silenciosamente, devolviendo listas vacías o valores nulos (None).

 - El programa podría interrumpirse y arrojar errores (como un AttributeError al intentar aplicar .text sobre un elemento que no fue encontrado).

 - Obliga a tener que darle mantenimiento constante al código del scraper cada vez que la página objetivo se actualiza.

## 2. Procesamiento y estructuración
### Pregunta 3:  ¿Por qué normalizar los títulos antes de implementar la búsqueda?

Normalizar los títulos (como convertirlos a minúsculas y eliminar espacios en blanco sobrantes) es fundamental porque los algoritmos de vectorización de texto (como TF-IDF) y las comparaciones de cadenas son estrictamente sensibles a la estructura exacta de los caracteres.

    - Si no se normalizan los textos antes de la búsqueda, podria generar diferentes problemas:

    - Se duplica el vocabulario innecesariamente: El modelo consideraría "Music", "MUSIC" y "music" como tres palabras completamente diferentes y sin relación entre sí.

    - Se pierde precisión en la recuperación: Si un usuario busca "ciencia" en minúsculas, el buscador no encontraría un libro titulado "Ciencia", ya que para la computadora no hay coincidencia exacta de los términos.

    - Se evitan errores por formato: Eliminar los espacios sobrantes al inicio o al final evita que un título como "  El Principito  " sea tratado de forma diferente a "El Principito".

En resumen, la normalización estandariza los datos para garantizar que la coincidencia entre la consulta del usuario y el índice de títulos sea precisa, justa e independiente de cómo se hayan utilizado las mayúsculas o los espacios originalmente.

## 3. Procesamiento y estructuración
### Pregunta 4:  En el código entregado, ¿qué función cumple fit_transform() sobre los títulos y por qué se usa transform() para la consulta?

En el código entregado, ambas funciones juegan un rol fundamental para que la comparación de textos funcione matemáticamente:

-   `fit_transform()` sobre los títulos: Cumple una doble función. Primero, "aprende" (fit) el vocabulario completo de todos los libros disponibles en el dataset, calculando las métricas de frecuencia e importancia de cada palabra. Segundo, "transforma" (transform) todos esos títulos en una matriz numérica (vectores TF-IDF) basada en ese vocabulario general.


-   `transform()` para la consulta: Se utiliza para convertir el texto que ingresa el usuario en un vector numérico, pero reutilizando estrictamente el vocabulario que ya se aprendió de los libros. Es vital usar solo `transform` aquí, porque la consulta debe ubicarse en el mismo espacio matemático (mismas dimensiones) que los títulos para poder usar la similitud del coseno. Si usáramos `fit` en la consulta, el modelo olvidaría el vocabulario de los libros, aprendería un diccionario nuevo basado únicamente en la frase del usuario, y sería imposible compararlos.

En resumen: `fit_transform` construye el "diccionario" base y vectoriza el catálogo, mientras que `transform` traduce las nuevas búsquedas apoyándose en ese mismo "diccionario" para que ambos hablen en el mismo formato.

### Pregunta 5: Si dos libros obtienen similitudes de 0.75 y 0.20 para la misma consulta, ¿cuál se muestra primero? Explique qué indica una puntuación cercana a cero.

El libro con la similitud de 0.75 se mostrará primero. Esto se debe a que el buscador ordena los resultados de mayor a menor puntuación para priorizar los documentos más relevantes.

Una puntuación cercana (o igual) a cero indica que prácticamente hay una ausencia de términos compartidos en el vocabulario entre la consulta del usuario y el título del libro. Es decir, los vectores no apuntan en la misma dirección, lo que significa que el texto buscado y el título del libro no tienen palabras en común.

## 4. Validación, análisis y entrega 

### PASO 12: Registro de resultados en README.md

| Caso | Consulta utilizada | Resultado observado | Estado |
| --- | --- | --- | --- |
| **T1** | `atticc` | Similitud positiva 0.576 . | Cumple |
| **T2** | `chile` | El programa mostró correctamente el mensaje "No se encontraron coincidencias.  | Cumple |
| **T3** | `ATTIC` |  Similitud positiva 0.576  . | Cumple |
| **T4** | `[vacía]`  | El programa mostró el mensaje "No se encontraron Coincidencias" | Cumple |


### PASO 13
 Cantidad de libros extraidos: 20
 Precio Promedio: 38.05 
 Consultas: 
 - Attic: A Light in the Attic | Precio: 51.77 | Similitud: 0.5760
 - Tipping: Tipping the Velvet | Precio: 53.74 | Similitud: 0.6679


### Pregunta 6: ¿Qué limitación tiene buscar solo por palabras presentes en títulos mediante TF-IDF? Proponga una mejora concreta.

La principal limitación que encontramos como grupo sobre usar TF-IDF exclusivamente en los títulos es que depende de coincidencias léxicas exactas y, como señala el documento, "no equivale a comprender el significado del texto". Esto significa que el buscador no es capaz de reconocer sinónimos (ej. buscar "coche" y que el título diga "automóvil"), no tolera errores ortográficos y carece de contexto. Además, al ser los títulos textos muy cortos, el factor de "frecuencia" (TF) pierde utilidad y el vocabulario disponible para encontrar coincidencias es sumamente reducido.

En cuanto a la mejora concreta, como grupo creemos que lo mejor seria concatenar el título con la descripción del libro y su categoría/auto antes de aplicar `fit_transform()`, creando un índice mucho más rico en vocabulario.








