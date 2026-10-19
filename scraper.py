import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def obtener_libros():
    respuesta = requests.get(URL, timeout=10)
    respuesta.raise_for_status()

    soup = BeautifulSoup(respuesta.text, "html.parser")
    elementos = soup.select("article.product_pod")
    libros = []

    equivalencias = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    for elemento in elementos:
        # Titulo
        titulo_html = elemento.select_one("h3 a")
        titulo = titulo_html.get("title", "").strip() if titulo_html else None

        precio_html = elemento.select_one(".price_color")
        precio = None

        if precio_html:
            texto_precio = precio_html.get_text(strip=True)
            texto_precio = texto_precio.replace("£", "").replace("Â", "").strip()

            try:
                precio = float(texto_precio)
            except ValueError:
                print(f"Aviso: precio no válido para {titulo}")

        disponibilidad_html = elemento.select_one(".availability")
        disponibilidad = (
            disponibilidad_html.get_text(" ", strip=True)
            if disponibilidad_html else None
        )

        rating_html = elemento.select_one(".star-rating")
        calificacion = None

        if rating_html:
            clases = rating_html.get("class", [])
            for clase in clases:
                if clase in equivalencias:
                    calificacion = equivalencias[clase]
                    break

        registro = {
            "titulo": titulo,
            "precio": precio,
            "disponibilidad": disponibilidad,
            "calificacion": calificacion
        }

        if any(valor is None for valor in registro.values()):
            print(f"Aviso: hay datos faltantes en el libro: {titulo}")

        libros.append(registro)

    return libros

if __name__ == "__main__":
    libros = obtener_libros()
    print(f"Total de libros extraídos: {len(libros)}")
    print(libros[:5])