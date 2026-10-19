import pandas as pd
from scraper import obtener_libros


def procesar_libros():
    libros = obtener_libros()
    df = pd.DataFrame(
        libros,
        columns=["titulo", "precio", "disponibilidad", "calificacion"]
    )

    print("\n--- PASO 5: INFORMACION INICIAL ---")
    print(df.head())

    print("\nInformacion y tipos de columnas:")
    df.info()

    print("\nDimensiones (filas, columnas):")
    print(df.shape)

    print("\nColumnas:")
    print(df.columns.tolist())

    for columna in ["titulo", "disponibilidad"]:
        df[columna] = df[columna].map(
            lambda valor: valor.strip() if isinstance(valor, str) else valor
        )

    df["titulo_normalizado"] = df["titulo"].map(
        lambda valor: valor.lower() if isinstance(valor, str) else valor
    )

    cantidad_antes = len(df)
    df = df.drop_duplicates(subset="titulo_normalizado", keep="first").copy()
    eliminados = cantidad_antes - len(df)

    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["calificacion"] = pd.to_numeric(df["calificacion"], errors="coerce")

    print("\n--- PASO 6: DATOS LIMPIOS ---")
    print(f"Duplicados eliminados: {eliminados}")
    print(df.dtypes)
    print("\nPrimeras cinco filas limpias:")
    print(df.head())

    cantidad_libros = len(df)
    precio_promedio = df["precio"].mean()

    print("\n--- PASO 7: ESTADISTICAS ---")
    print(f"Cantidad de libros: {cantidad_libros}")

    if pd.notna(precio_promedio):
        print(f"Precio promedio: £{precio_promedio:.2f}")
    else:
        print("Precio promedio: no disponible")

    df.to_csv("libros.csv", index=False, encoding="utf-8")

    print("\nArchivo libros.csv guardado correctamente.")

    return df

if __name__ == "__main__":
    df = procesar_libros()