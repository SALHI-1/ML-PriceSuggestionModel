import pandas as pd
import numpy as np
import random

# Configuration
num_rows = 3000
eth_to_wei = 10**18

# 1. Structure de données : Pays -> Villes -> {lat, lon, price_factor}
# Le price_factor simule le coût de la vie relatif en ETH
world_data = {
    'Morocco': {
        'factor': 1.0,
        'cities': {
            'Casablanca': [33.5731, -7.5898, 1.3],
            'Marrakech': [31.6295, -7.9811, 1.2],
            'Rabat': [34.0209, -6.8416, 1.2],
            'Tangier': [35.7595, -5.8340, 1.1]
        }
    },
    'France': {
        'factor': 3.5,
        'cities': {
            'Paris': [48.8566, 2.3522, 2.5],
            'Lyon': [45.7640, 4.8357, 1.5],
            'Marseille': [43.2965, 5.3698, 1.3],
            'Nice': [43.7102, 7.2620, 1.8]
        }
    },
    'Spain': {
        'factor': 2.5,
        'cities': {
            'Madrid': [40.4168, -3.7038, 1.8],
            'Barcelona': [41.3851, 2.1734, 2.0],
            'Valencia': [39.4699, -0.3763, 1.3],
            'Sevilla': [37.3891, -5.9845, 1.1]
        }
    },
    'USA': {
        'factor': 4.5,
        'cities': {
            'New York': [40.7128, -74.0060, 3.0],
            'Los Angeles': [34.0522, -118.2437, 2.5],
            'Miami': [25.7617, -80.1918, 2.2],
            'Chicago': [41.8781, -87.6298, 1.8]
        }
    },
    'UAE': {
        'factor': 4.0,
        'cities': {
            'Dubai': [25.2048, 55.2708, 2.8],
            'Abu Dhabi': [24.4539, 54.3773, 2.2]
        }
    }
}

data = []

for i in range(num_rows):
    # Sélection aléatoire
    country = random.choice(list(world_data.keys()))
    city = random.choice(list(world_data[country]['cities'].keys()))
    
    city_info = world_data[country]['cities'][city]
    country_factor = world_data[country]['factor']
    
    # Coordonnées avec léger bruit
    lat = city_info[0] + random.uniform(-0.08, 0.08)
    lon = city_info[1] + random.uniform(-0.08, 0.08)
    city_factor = city_info[2]
    
    # Caractéristiques physiques
    sqm = random.randint(20, 350)
    total_rooms = max(1, int(sqm / 40) + random.randint(0, 2))
    nombre_etoiles = random.randint(1, 5)
    
    # --- LOGIQUE DE PRIX (ETH) ---
    # Base : 0.0005 ETH par m2
    base_eth = sqm * 0.0005
    # Application des multiplicateurs
    final_eth = base_eth * country_factor * city_factor
    # Bonus standing (étoiles)
    final_eth += (nombre_etoiles * 0.08 * country_factor)
    
    # Bruit de marché (+/- 15%)
    final_eth *= random.uniform(0.85, 1.15)
    
    # Conversion en Wei
    rental_rent_wei = int(final_eth * eth_to_wei)
    
    data.append([
        city, country, lon, lat, sqm, total_rooms, 
        "MONTHLY", nombre_etoiles, rental_rent_wei
    ])

# 2. DataFrame et Export
columns = ['city', 'country', 'longitude', 'latitude', 'sqm', 'total_rooms', 'typeOfRental', 'nombre_etoiles', 'rental_rent']
df = pd.DataFrame(data, columns=columns)
df.to_csv('property_global_data_wei.csv', index=False)

print(f"Dataset international de {num_rows} lignes généré !")
print(df.groupby('country')['rental_rent'].mean() / eth_to_wei) # Affiche prix moyen en ETH par pays