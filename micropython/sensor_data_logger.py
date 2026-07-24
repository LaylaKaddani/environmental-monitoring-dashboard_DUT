from machine import Pin, ADC
import dht
import time
import uos

# Configuration des capteurs
dht_sensor = dht.DHT11(Pin(16))  # GPIO16 pour le DHT11
water_sensor = Pin(17, Pin.IN)   # GPIO17 pour le capteur d'eau
light_sensor = ADC(Pin(26))      # ADC0 (GPIO26) pour la photorésistance

# Vérifier et créer le dossier CSV
def ensure_csv_folder_exists():
    if "csv" not in uos.listdir():
        uos.mkdir("csv")

# Fonction pour écrire dans un fichier CSV unique
def save_data_to_csv(data):
    ensure_csv_folder_exists()
    file_path = "csv/sensor_data.csv"
    date_time = time.localtime()
    date_time_str = f"{date_time[0]}-{date_time[1]:02d}-{date_time[2]:02d} {date_time[3]:02d}:{date_time[4]:02d}:{date_time[5]:02d}"
    try:
        # Ouvrir le fichier en mode append
        with open(file_path, mode="a") as file:
            # Ajouter l'en-tête si le fichier est vide
            if uos.stat(file_path)[6] == 0:
                file.write("datetime,temperature,humidity,water,light\n")
            # Écrire les données
            file.write(f"{date_time_str},{data['temperature']},{data['humidity']},{data['water']},{data['light']}\n")
    except Exception as e:
        print(f"Erreur d'écriture dans le fichier CSV : {e}")

# Lecture des données des capteurs
def read_sensors():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except Exception as e:
        temperature = None
        humidity = None
        print(f"Erreur DHT11 : {e}")
    
    water_detected = water_sensor.value()
    light_intensity = light_sensor.read_u16()  # Lecture ADC en 16 bits

    return {
        "temperature": round(temperature, 2) if temperature is not None else None,
        "humidity": round(humidity, 2) if humidity is not None else None,
        "water": water_detected,
        "light": light_intensity
    }

# Enregistrement continu des données
def collect_and_save_data():
    while True:
        sensor_data = read_sensors()

        # Sauvegarder les données dans un fichier CSV unique
        save_data_to_csv(sensor_data)

        # Afficher les données pour le débogage
        print(f"Temperature: {sensor_data['temperature']}°C, Humidity: {sensor_data['humidity']}%, "
              f"Water: {sensor_data['water']}, Light: {sensor_data['light']}")

        # Pause de 5 secondes
        time.sleep(5)

# Lancer le programme
try:
    collect_and_save_data()
except KeyboardInterrupt:
    print("Arrêt du programme.")
