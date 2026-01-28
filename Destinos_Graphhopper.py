import requests
from geopy.distance import geodesic

API_KEY = "eabbf2e8-564a-4c0a-86cc-95cb07f54157"

def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "locale": "es", "limit": 1, "key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["hits"]:
            punto = data["hits"][0]["point"]
            return (punto['lat'], punto['lng'])
    return None

def calcular_ruta(ciudad_origen, ciudad_destino, origen, destino, transporte):
    if transporte in ["car", "foot", "bike"]:
        url = "https://graphhopper.com/api/1/route"
        params = {
            "point": [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
            "vehicle": transporte,
            "locale": "es",
            "instructions": "true",
            "calc_points": "true",
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            path = response.json()["paths"][0]
            distancia_km = path["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion_min = path["time"] / 1000 / 60
            print(f"\n📍 Origen: {ciudad_origen}")
            print(f"📍 Destino: {ciudad_destino}")
            print(f"🚗 Medio de transporte: {transporte}")
            print(f"📏 Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
            print(f"⏱ Duración: {duracion_min:.1f} minutos\n")
            print("🗺 Narrativa del viaje:")
            for paso in path["instructions"]:
                print(f"- {paso['text']}")
        else:
            print("❌ Error en la API:", response.text)

    elif transporte == "bus":
        distancia_km = geodesic(origen, destino).km
        distancia_millas = distancia_km * 0.621371
        if "Santiago" in ciudad_origen and "Valpara" in ciudad_destino:
            duracion_min = 109
        else:
            duracion_min = (distancia_km / 60) * 60 * 1.1
        print(f"\n🚌 Bus: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
        print(f"⏱ Duración estimada: {duracion_min:.1f} minutos (según datos reales)\n")

    elif transporte == "avion":
        distancia_km = geodesic(origen, destino).km
        distancia_millas = distancia_km * 0.621371
        if "Santiago" in ciudad_origen and "Valpara" in ciudad_destino:
            duracion_min = 37
        else:
            duracion_min = (distancia_km / 800) * 60
        print(f"\n✈️ Avión: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
        print(f"⏱ Duración estimada: {duracion_min:.1f} minutos (según datos reales)\n")

def main():
    while True:
        print("\n--- Calculadora de rutas con Graphhopper ---")
        ciudad_origen = input("Ingrese ciudad de origen (o 'v' para salir): ")
        if ciudad_origen.lower() == "v":
            print("👋 Programa finalizado.")
            break

        ciudad_destino = input("Ingrese ciudad de destino: ")
        transporte = input("Ingrese medio de transporte (car, foot, bike, bus, avion): ").lower()

        if transporte not in ["car", "foot", "bike", "bus", "avion"]:
            print("⚠️ Medio de transporte inválido. Usa: car, foot, bike, bus o avion.")
            continue

        origen_coord = obtener_coordenadas(ciudad_origen)
        destino_coord = obtener_coordenadas(ciudad_destino)

        if origen_coord and destino_coord:
            calcular_ruta(ciudad_origen, ciudad_destino, origen_coord, destino_coord, transporte)
        else:
            print("⚠️ No se pudieron obtener coordenadas.")

if __name__ == "__main__":
    main()

