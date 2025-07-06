import requests

API_KEY = "7a4611cb-0c87-4e04-b706-50b0a57956dc"
BASE_URL_GEOCODE = "https://graphhopper.com/api/1/geocode"
BASE_URL_ROUTE = "https://graphhopper.com/api/1/route"

def obtener_coordenadas(ciudad, pais):
    params = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    respuesta = requests.get(BASE_URL_GEOCODE, params=params)
    datos = respuesta.json()

    if datos.get("hits"):
        punto = datos["hits"][0]["point"]
        return punto["lat"], punto["lng"]
    else:
        return None

def calcular_ruta(origen, destino, medio):
    params = {
        "point": [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
        "vehicle": medio,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    }
    respuesta = requests.get(BASE_URL_ROUTE, params=params)
    return respuesta.json()

# Programa principal
while True:
    print("\n=== Calculadora de viaje Chile → Argentina ===")
    ciudad_origen = input("Ciudad de origen (Chile) (o 's' para salir): ").strip()
    if ciudad_origen.lower() == 's':
        break

    ciudad_destino = input("Ciudad de destino (Argentina) (o 's' para salir): ").strip()
    if ciudad_destino.lower() == 's':
        break

    medio = input("Medio de transporte (car, bike, foot): ").strip().lower()

    coordenadas_origen = obtener_coordenadas(ciudad_origen, "Chile")
    coordenadas_destino = obtener_coordenadas(ciudad_destino, "Argentina")

    if coordenadas_origen and coordenadas_destino:
        datos_ruta = calcular_ruta(coordenadas_origen, coordenadas_destino, medio)

        try:
            ruta = datos_ruta["paths"][0]
            distancia_km = ruta["distance"] / 1000
            distancia_millas = ruta["distance"] * 0.000621371
            duracion_horas = ruta["time"] / (1000 * 60 * 60)

            print(f"\n🛣️ Ruta desde {ciudad_origen.title()} (Chile) a {ciudad_destino.title()} (Argentina):")
            print(f"→ Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
            print(f"→ Duración estimada: {duracion_horas:.2f} horas")

            print("\n📋 Instrucciones del viaje:")
            for paso in ruta["instructions"]:
                print(f"- {paso['text']}")

        except Exception as e:
            print("❌ No se pudo calcular la ruta:", e)
    else:
        print("⚠️ No se pudieron encontrar coordenadas para una o ambas ciudades.")
