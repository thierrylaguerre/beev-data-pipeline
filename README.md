# Beev Data Pipeline 

## Installation

1. **Installer Docker Desktop**  
   - Télécharger et installer [Docker Desktop](https://www.docker.com/products/docker-desktop/).
   - Vérifier que Docker fonctionne avec :  
     ```sh
     docker --version
     ```

2. **Lancer la base de données**  
   ```sh
   docker-compose up -d
   ```

3. **Installer les dépendances**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Importer les fichiers CSV**  
   ```sh
   python script_import_data.py
   ```

5. **Exécuter les requêtes SQL avec pgAdmin**  
   - Ouvrir **pgAdmin** et se connecter à la base de données.
   - Exécuter les requêtes du fichier `queries.sql` dans l'éditeur SQL de pgAdmin.

6. **Générer les graphiques**  
   ```sh
   python script_graph.py
   ```

---

## Explication du fichier `script_import_data.py`

Ce script permet de :  
- **Créer les tables** `car_data` et `consumer_data` dans la base PostgreSQL si elles n'existent pas.
- **Lire les fichiers CSV** contenant les données des voitures et des consommateurs.
- **Insérer ces données** dans la base de données.
- **Gérer les erreurs** et **afficher des logs** en cas de problème.


### **Détail des fonctions**

#### `get_db_connection()`
Établit une connexion à la base de données PostgreSQL avec les paramètres définis dans `DB_PARAMS`.

#### `create_tables()`
Crée les tables nécessaires (`car_data` et `consumer_data`) si elles n'existent pas déjà.

#### `insert_car_data(csv_file)`
- Vérifie si le fichier CSV des voitures existe et s'il est valide.
- Charge les données dans un DataFrame pandas. 
- Insère les données dans la table `car_data`.

#### `insert_consumer_data(csv_file)`
- Vérifie si le fichier CSV des consommateurs existe et s'il est valide.
- Charge les données dans un DataFrame pandas. (J'ai détecter un probleme au niveau des noms des colonnes. Il manquait le nom de la colonne des marques de voitures. Pour résoudre ce probleme, j'ai attributer aux colonnes du dataset leur noms respectives pendant le chargement des données dans un dataframe Pandas) 
- Insère les données dans la table `consumer_data`.

#### `main()`
- Lance tout le processus : création des tables, insertion des données.
- Utilise des logs pour suivre l'avancement du script.

---

## Explication du fichier `script_graph.py`

Ce script génère deux graphiques pour analyser le marché des voitures électriques et thermiques.

- **Premier graphique :** Compare le volume des ventes des voitures électriques vs thermiques par année.
- **Deuxième graphique :** Compare la valeur des ventes (prix * volume) des voitures électriques vs thermiques par année.

### **Détail des étapes**

#### Connexion à la base de données
Le script utilise **SQLAlchemy** pour se connecter à PostgreSQL et exécuter les requêtes.

#### Requête SQL pour le volume des ventes
- Récupère le **nombre total de voitures vendues** chaque année.
- Regroupe les résultats par **année** et **type de moteur**.

#### Requête SQL pour la valeur des ventes
- Calcule la **valeur totale des ventes** chaque année (**prix * volume**).
- Regroupe les résultats par **année** et **type de moteur**.

#### Génération des graphiques avec Matplotlib
- **Premier graphique :** Évolution du **volume des ventes** des voitures électriques vs thermiques.
- **Deuxième graphique :** Évolution de la **valeur des ventes** des voitures électriques vs thermiques.
