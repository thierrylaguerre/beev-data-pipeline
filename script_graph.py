import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuration de la base de données
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_db"

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# Requête SQL pour récupérer les volumes de ventes par année et type de moteur
query_volume = """
SELECT c.year, car.engine_type, SUM(c.sales_volume) AS total_sales
FROM car_data car
JOIN consumer_data c ON car.model = c.model
GROUP BY c.year, car.engine_Type
ORDER BY c.year;
"""
df_volume = pd.read_sql(query_volume, engine)

# Requête SQL pour récupérer la valeur des ventes par année et type de moteur
query_value = """
SELECT c.year, car.engine_type, SUM(car.price * c.sales_volume) AS total_value
FROM car_data car
JOIN consumer_data c ON car.model = c.model
GROUP BY c.year, car.engine_type
ORDER BY c.year;
"""
df_value = pd.read_sql(query_value, engine)

# Création du graphique pour le volume des ventes
plt.figure(figsize=(10, 5))
for engine_type in df_volume['engine_type'].unique():
    data = df_volume[df_volume['engine_type'] == engine_type]
    plt.plot(data['year'], data['total_sales'], marker='o', label=engine_type)
plt.ticklabel_format(style='plain', axis='y')
plt.xlabel("Année")
plt.ylabel("Volume de ventes")
plt.title("Volume des ventes des voitures électriques vs thermiques")
plt.legend()
plt.grid()
plt.show()

# Création du graphique pour la valeur des ventes
plt.figure(figsize=(10, 5))
for engine_type in df_value['engine_type'].unique():
    data = df_value[df_value['engine_type'] == engine_type]
    plt.plot(data['year'], data['total_value'], marker='o', label=engine_type)
plt.ticklabel_format(style='plain', axis='y')
plt.xlabel("Année")
plt.ylabel("Valeur totale des ventes ($)")
plt.title("Valeur des ventes des voitures électriques vs thermiques")
plt.legend()
plt.grid()
plt.show()

