# import pandas as pd
# import numpy as np
# import random
# from pathlib import Path
# # Configuration
# num_rows = 3000
# eth_to_wei = 10**18

# world_data = {
#     'Morocco': {
#         'factor': 1.0,
#         'cities': {
#             'Casablanca': [33.5731, -7.5898, 1.3],
#             'Marrakech': [31.6295, -7.9811, 1.5], # Plus cher en daily (tourisme)
#             'Rabat': [34.0209, -6.8416, 1.2],
#             'Tangier': [35.7595, -5.8340, 1.4]  # Plus cher en daily (mer)
#         }
#     },
#     'France': {
#         'factor': 3.5,
#         'cities': {
#             'Paris': [48.8566, 2.3522, 2.8],
#             'Lyon': [45.7640, 4.8357, 1.6],
#             'Marseille': [43.2965, 5.3698, 1.5],
#             'Nice': [43.7102, 7.2620, 2.2]
#         }
#     },
#     'Spain': {
#         'factor': 2.8,
#         'cities': {
#             'Madrid': [40.4168, -3.7038, 1.8],
#             'Barcelona': [41.3851, 2.1734, 2.3],
#             'Valencia': [39.4699, -0.3763, 1.6],
#             'Sevilla': [37.3891, -5.9845, 1.4]
#         }
#     },
#     'USA': {
#         'factor': 4.5,
#         'cities': {
#             'New York': [40.7128, -74.0060, 3.2],
#             'Los Angeles': [34.0522, -118.2437, 2.7],
#             'Miami': [25.7617, -80.1918, 2.8],
#             'Chicago': [41.8781, -87.6298, 1.9]
#         }
#     },
#     'UAE': {
#         'factor': 4.2,
#         'cities': {
#             'Dubai': [25.2048, 55.2708, 3.0],
#             'Abu Dhabi': [24.4539, 54.3773, 2.4]
#         }
#     }
# }

# data = []

# for i in range(num_rows):
#     country = random.choice(list(world_data.keys()))
#     city = random.choice(list(world_data[country]['cities'].keys()))
    
#     city_info = world_data[country]['cities'][city]
#     country_factor = world_data[country]['factor']
    
#     # Coordonnées et facteurs locaux
#     lat = city_info[0] + random.uniform(-0.05, 0.05)
#     lon = city_info[1] + random.uniform(-0.05, 0.05)
#     city_factor = city_info[2]
    
#     # --- Nouvelles Caractéristiques Daily ---
#     sqm = random.randint(15, 200) # Souvent plus petit que le mensuel
#     total_rooms = max(1, int(sqm / 35) + random.randint(0, 1))
#     max_guests = total_rooms * 2 + random.randint(-1, 2)
#     max_guests = max(1, max_guests)
    
#     has_wifi = random.choice([0, 1])
#     has_pool = random.choice([0, 1]) if sqm > 50 else 0
    
#     # Distance (en km) : plus on est proche (0), plus c'est cher
#     dist_center = round(random.uniform(0.1, 15.0), 2)
#     dist_sea = round(random.uniform(0.1, 20.0), 2)
    
#     nombre_etoiles = random.randint(1, 5)
    
#     # --- LOGIQUE DE PRIX DAILY (ETH) ---
#     # Base quotidienne plus élevée proportionnellement au mensuel
#     base_eth = sqm * 0.00005 
    
#     # Multiplicateurs géo
#     final_eth = base_eth * country_factor * city_factor
    
#     # Impact des invités (plus de monde = plus cher)
#     final_eth += (max_guests * 0.002 * country_factor)
    
#     # Impact de la mer (Bonus énorme si < 2km)
#     if dist_sea < 2:
#         final_eth *= 1.4
#     elif dist_sea < 5:
#         final_eth *= 1.15
        
#     # Impact du centre (Bonus si < 3km)
#     if dist_center < 3:
#         final_eth *= 1.2
        
#     # Bonus équipements
#     if has_pool: final_eth += (0.015 * country_factor)
#     if has_wifi: final_eth += (0.002 * country_factor)
    
#     # Standing
#     final_eth += (nombre_etoiles * 0.01 * country_factor)
    
#     # Bruit de marché
#     final_eth *= random.uniform(0.9, 1.1)
    
#     # Conversion Wei
#     rental_rent_wei = int(final_eth * eth_to_wei)
    
#     data.append([
#         city, country, lon, lat, sqm, total_rooms, max_guests,
#         has_wifi, has_pool, dist_center, dist_sea,
#         "DAILY", nombre_etoiles, rental_rent_wei
#     ])

# # Colonnes mises à jour
# columns = [
#     'city', 'country', 'longitude', 'latitude', 'sqm', 'total_rooms', 'max_guests',
#     'has_wifi', 'has_pool', 'distance_to_center', 'distance_to_sea',
#     'typeOfRental', 'nombre_etoiles', 'rental_rent'
# ]

# df = pd.DataFrame(data, columns=columns)

# # Sauvegarde
# # Récupère le chemin du dossier où se trouve le script de génération
# current_dir = Path(__file__).resolve().parent
# file_path = current_dir / 'property_daily_data_wei.csv'
# df.to_csv(file_path, index=False)

# print(f"Dataset Daily de {num_rows} lignes généré avec succès !")
# print(f"Fichier : {file_path}")
# # Moyenne par pays pour vérification (en ETH)
# print(df.groupby('country')['rental_rent'].mean() / eth_to_wei)


import pandas as pd
import numpy as np
import random
from pathlib import Path

# Configuration
num_rows = 3000
eth_to_wei = 10**18

# 1. Structure de données identique au script Monthly
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
    
    # --- LOGIQUE DE PRIX DAILY (ETH) ---
    # Un prix journalier est environ 20 à 30 fois plus petit qu'un loyer mensuel
    # Base : 0.00002 ETH par m2 (au lieu de 0.0005 pour le mensuel)
    base_eth_daily = sqm * 0.00002
    
    # Application des multiplicateurs
    final_eth = base_eth_daily * country_factor * city_factor
    
    # Bonus standing (étoiles) adapté au prix journalier
    final_eth += (nombre_etoiles * 0.004 * country_factor)
    
    # Bruit de marché (+/- 15%)
    final_eth *= random.uniform(0.85, 1.15)
    
    # Conversion en Wei
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