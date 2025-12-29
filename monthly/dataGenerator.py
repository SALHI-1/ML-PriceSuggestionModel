import pandas as pd
import numpy as np
import random
from pathlib import Path

# Configuration
num_rows = 3000
eth_to_wei = 10**18
mad_to_eth = 1 / 25000  # Conversion basée sur 1 ETH = 25.000 DH

# 1. Structure de données : Uniquement le Maroc avec 12 villes
# [latitude, longitude, price_factor_ville]
# Les facteurs sont ajustés selon le coût du loyer local
morocco_data = {
    'Morocco': {
        'cities': {
            'Casablanca': [33.5731, -7.5898, 1.5],   # Économique, très cher
            'Rabat': [34.0209, -6.8416, 1.45],      # Capitale, cher
            'Marrakech': [31.6295, -7.9811, 1.3],   # Touristique
            'Tangier': [35.7595, -5.8340, 1.25],    # Nord en expansion
            'Agadir': [30.4278, -9.5981, 1.1],      # Touristique Sud
            'Fes': [34.0331, -5.0003, 0.85],        # Historique, abordable
            'Meknes': [33.8935, -5.5473, 0.8],      # Abordable
            'Oujda': [34.6805, -1.9076, 0.7],       # Oriental, moins cher
            'Kenitra': [34.2570, -6.5890, 0.95],    # Proche Rabat
            'Tetouan': [35.5785, -5.3684, 1.0],     # Nord
            'El Jadida': [33.2316, -8.5007, 0.9],   # Industriel/Etudiant
            'Nador': [35.1681, -2.9335, 1.0]        # Portuaire
        }
    }
}

data = []

for i in range(num_rows):
    country = 'Morocco'
    city = random.choice(list(morocco_data[country]['cities'].keys()))
    
    city_info = morocco_data[country]['cities'][city]
    
    # Coordonnées avec léger bruit pour simuler différents quartiers
    lat = city_info[0] + random.uniform(-0.04, 0.04)
    lon = city_info[1] + random.uniform(-0.04, 0.04)
    city_factor = city_info[2]
    
    # Caractéristiques physiques
    sqm = random.randint(40, 180) # Appartements standards marocains
    total_rooms = max(1, int(sqm / 40) + random.randint(0, 1))
    nombre_etoiles = random.randint(1, 5)
    
    # --- LOGIQUE DE PRIX (Calibrée en MAD puis convertie en ETH) ---
    # Base : environ 40 DH par m2
    base_mad = sqm * 45 
    
    # Application du facteur ville (ex: Casa = 1.5 * base)
    final_mad = base_mad * city_factor
    
    # Bonus Standing (Étoiles) : de 500 DH à 2500 DH en plus
    final_mad += (nombre_etoiles * 500)
    
    # Bruit de marché (+/- 10%)
    final_mad *= random.uniform(0.9, 1.1)
    
    # --- CONVERSION ---
    # On s'assure que le prix reste dans la fourchette 2000 - 15000 DH
    final_mad = max(2000, min(final_mad, 16000))
    
    # Conversion MAD -> ETH -> Wei
    final_eth = final_mad * mad_to_eth
    rental_rent_wei = int(final_eth * eth_to_wei)
    
    data.append([
        city, country, lon, lat, sqm, total_rooms, 
        "MONTHLY", nombre_etoiles, rental_rent_wei
    ])
# 2. DataFrame et Export
columns = ['city', 'country', 'longitude', 'latitude', 'sqm', 'total_rooms', 'typeOfRental', 'nombre_etoiles', 'rental_rent']
df = pd.DataFrame(data, columns=columns)


# Sauvegarde dans le même dossier que le script
current_dir = Path(__file__).resolve().parent
file_path = current_dir / 'property_monthly_data_wei.csv'
df.to_csv(file_path, index=False)


print(f"Dataset international de {num_rows} lignes généré !")
print(df.groupby('country')['rental_rent'].mean() / eth_to_wei) # Affiche prix moyen en ETH par pays