import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

libros = pd.read_csv("libros.csv")

libros = libros.dropna(subset=["titulo_normalizado"]).copy()
libros["titulo_normalizado"] = (
    libros["titulo_normalizado"].astype(str).str.strip()
)
libros = libros[libros["titulo_normalizado"] != ""].reset_index(drop=True)

if libros.empty:
    raise ValueError("No hay títulos válidos para construir el buscador.")

vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(libros["titulo_normalizado"])

def buscar(consulta: str, top_k: int = 5):
    consulta = consulta.strip().lower()

    if not consulta:
        print("Ingrese una consulta no vacía.")
        return []

    if top_k <= 0:
        return []

    vector_consulta = vectorizador.transform([consulta])

    puntuaciones = cosine_similarity(
        vector_consulta, matriz_tfidf
    ).ravel()

    indices = puntuaciones.argsort()[::-1]

    resultados = []

    for i in indices:
        if puntuaciones[i] <= 0:
            break

        resultados.append({
            "titulo": libros.iloc[i]["titulo"],
            "precio": libros.iloc[i]["precio"],
            "similitud": float(puntuaciones[i])
        })

        if len(resultados) >= top_k:
            break

    return resultados


if __name__ == "__main__":
    consulta = input("Ingrese una palabra o título: ")
    resultados = buscar(consulta, top_k=3) #Esto es para mostrar los 3 primeros resultados

    if not resultados:
        print("No se encontraron coincidencias.")
    else:
        print("\nResultados de búsqueda:")
        for r in resultados:
            print(
                f"{r['titulo']} | Precio: £{r['precio']:.2f} | "
                f"Similitud: {r['similitud']:.4f}"
            )