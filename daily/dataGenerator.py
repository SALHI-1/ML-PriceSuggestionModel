import pandas as pd
import numpy as np
import random
from pathlib import Path

# Configuration
num_rows = 3000
eth_to_wei = 10**18
mad_to_eth = 1 / 25000  # Basé sur 1 ETH ≈ 25.000 DH

# 1. Structure de données : 12 villes du Maroc
# [latitude, longitude, price_factor_daily]
# Marrakech a ici le facteur le plus élevé car c'est la capitale du tourisme journalier
morocco_data = {
    'Morocco': {
        'cities': {
            'Marrakech': [31.6295, -7.9811, 1.6],   # Très forte demande journalière
            'Casablanca': [33.5731, -7.5898, 1.5],   # Business et tourisme
            'Rabat': [34.0209, -6.8416, 1.4],      # Capitale administrative
            'Tangier': [35.7595, -5.8340, 1.35],    # Porte de l'Europe
            'Agadir': [30.4278, -9.5981, 1.3],      # Station balnéaire
            'Chefchaouen': [35.1713, -5.2697, 1.2],  # Très prisé en "Daily"
            'Fes': [34.0331, -5.0003, 0.95],        # Culturel
            'Tetouan': [35.5785, -5.3684, 1.15],    # Côte Nord
            'Essaouira': [31.5125, -9.7701, 1.25],  # Touristique
            'Kenitra': [34.2570, -6.5890, 0.9],     # Urbain
            'Oujda': [34.6805, -1.9076, 0.75],      # Frontière
            'Meknes': [33.8935, -5.5473, 0.85]      # Historique
        }
    }
}

data = []

for i in range(num_rows):
    country = 'Morocco'
    city = random.choice(list(morocco_data[country]['cities'].keys()))
    
    city_info = morocco_data[country]['cities'][city]
    
    # Coordonnées avec bruit (quartiers différents)
    lat = city_info[0] + random.uniform(-0.04, 0.04)
    lon = city_info[1] + random.uniform(-0.04, 0.04)
    city_factor = city_info[2]
    
    # Caractéristiques physiques (les locations journalières sont souvent plus petites)
    sqm = random.randint(30, 150)
    total_rooms = max(1, int(sqm / 45) + random.randint(0, 1))
    nombre_etoiles = random.randint(1, 5)
    
    # --- LOGIQUE DE PRIX DAILY (Calculé en MAD) ---
    # Base : environ 5 DH par m2 par jour
    base_mad_daily = sqm * 5 
    
    # Application du facteur ville
    final_mad = base_mad_daily * city_factor
    
    # Bonus Standing (étoiles) : plus important en Daily (équipement, service)
    # Entre 150 DH et 750 DH de plus selon les étoiles
    final_mad += (nombre_etoiles * 150)
    
    # Bruit de marché (+/- 12%)
    final_mad *= random.uniform(0.88, 1.12)
    
    # --- CONVERSION ---
    # Fourchette cible : 300 DH - 3500 DH
    final_mad = max(300, min(final_mad, 4000))
    
    # MAD -> ETH -> Wei
    final_eth = final_mad * mad_to_eth
    rental_rent_wei = int(final_eth * eth_to_wei)
    
    data.append([
        city, country, lon, lat, sqm, total_rooms, 
        "DAILY", nombre_etoiles, rental_rent_wei
    ])
# 2. DataFrame et Export
columns = ['city', 'country', 'longitude', 'latitude', 'sqm', 'total_rooms', 'typeOfRental', 'nombre_etoiles', 'rental_rent']
df = pd.DataFrame(data, columns=columns)

# Sauvegarde dans le même dossier que le script
current_dir = Path(__file__).resolve().parent
file_path = current_dir / 'property_daily_data_wei.csv'
df.to_csv(file_path, index=False)

print(f"Dataset journalier de {num_rows} lignes généré avec succès !")
print(f"Prix moyen par pays (en ETH par jour) :")
print(df.groupby('country')['rental_rent'].mean() / eth_to_wei)