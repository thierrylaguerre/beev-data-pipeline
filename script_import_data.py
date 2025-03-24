import pandas as pd
import psycopg2
from psycopg2 import sql
import logging
import os

# Configuration de la base de données
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "test_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
}

# Configuration du logger pour suivre l'exécution du script
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Stucture des tables SQL
CREATE_TABLE_QUERY_CAR = """
CREATE TABLE IF NOT EXISTS car_data (
    id SERIAL PRIMARY KEY, 
    make TEXT NOT NULL,    
    model TEXT NOT NULL,   
    production_year INT NOT NULL,  
    price FLOAT NOT NULL,   
    engine_type TEXT NOT NULL 
);
"""

CREATE_TABLE_QUERY_CONSUMER = """
CREATE TABLE IF NOT EXISTS consumer_data (
    id SERIAL PRIMARY KEY, 
    country TEXT NOT NULL,
    brand TEXT NOT NULL,     
    model TEXT NOT NULL,   
    year INT NOT NULL,  
    review_score FLOAT NOT NULL,   
    sales_volume INT NOT NULL
);
"""
# La fonction établit une connexion à la base de données PostgreSQL.
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except psycopg2.DatabaseError as e:
        logging.error(f"Erreur de connexion à la base de données : {e}")
        raise
    
# La fonction crée les tables dans la base de données si elles n'existent pas.
def create_tables():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_QUERY_CAR)
                cur.execute(CREATE_TABLE_QUERY_CONSUMER)
                conn.commit()
                logging.info("Les tables 'car_data' et 'consumer_data' sont crées avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la création des tables : {e}")

# La fonction insère les données issues du fichier CSV des voitures dans la base de données.
def insert_car_data(csv_file):
    if not os.path.exists(csv_file):
        logging.error(f"Le fichier {csv_file} n'existe pas.")
        return
    
    df = pd.read_csv(csv_file, header=0)
    if df.empty:
        logging.warning("Le fichier CSV est vide.")
        return
    
    df.columns = ["make", "model", "production_year", "price", "engine_type"]
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                insert_query = sql.SQL("""
                    INSERT INTO car_data (make, model, production_year, price, engine_type)
                    VALUES (%s, %s, %s, %s, %s)
                """)
                
                for _, row in df.iterrows():
                    cur.execute(insert_query, (row["make"], row["model"], row["production_year"], row["price"], row["engine_type"]))
                
                conn.commit()
                logging.info(f"{len(df)} enregistrements insérés avec succès dans 'car_data'.")
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion des données voitures : {e}")

# Cette fonction insère les données issues du fichier CSV des consommateurs dans la base de données.
def insert_consumer_data(csv_file):
    
    if not os.path.exists(csv_file):
        logging.error(f"Le fichier {csv_file} n'existe pas.")
        return
    
    df = pd.read_csv(csv_file, names=["country", "brand", "model", "year", "review_score", "sales_volume"], header=0)
    if df.empty:
        logging.warning("Le fichier CSV est vide.")
        return
    
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                insert_query = sql.SQL("""
                    INSERT INTO consumer_data (country, brand, model, year, review_score, sales_volume)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """)
                
                for _, row in df.iterrows():
                    cur.execute(insert_query, (row["country"], row["brand"], row["model"], row["year"], row["review_score"], row["sales_volume"]))
                
                conn.commit()
                logging.info(f"{len(df)} enregistrements insérés avec succès dans 'consumer_data'.")
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion des données consommateurs : {e}")

def main():
    logging.info("Démarrage du script de traitement des données.")
    create_tables()
    car_csv_file = os.getenv("CAR_CSV_FILE", "car_data.csv")
    consumer_csv_file = os.getenv("CONSUMER_CSV_FILE", "consumer_data.csv")
    insert_car_data(car_csv_file)
    insert_consumer_data(consumer_csv_file)
    logging.info("Traitement terminé avec succès.")

if __name__ == "__main__":
    main()

