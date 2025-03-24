-- a. Nombre total de voitures par modèle et par pays
SELECT country, model, SUM(sales_volume) AS total_sales
FROM consumer_data
GROUP BY country, model
ORDER BY country, total_sales DESC;

-- b. Pays ayant le plus de chaque modèle et combien il en a
SELECT c.model, c.country, c.sales_volume
FROM consumer_data c
WHERE (c.model, c.sales_volume) IN (
    SELECT model, MAX(sales_volume)
    FROM consumer_data
    GROUP BY model
);

-- c. Modèles vendus aux États-Unis mais pas en France
SELECT DISTINCT c.model
FROM consumer_data c
WHERE c.country = 'United States'
AND c.model NOT IN (
    SELECT model FROM consumer_data WHERE country = 'France'
);

-- d. Prix moyen des voitures par pays et par type de moteur
SELECT cd.country, car.engine_type, AVG(car.Price) AS avg_price
FROM car_data car
JOIN consumer_data cd ON car.model = cd.model
GROUP BY cd.country, car.engine_type;

-- e. Évaluations moyennes des voitures électriques vs thermiques
SELECT car.engine_type, AVG(cd.review_score) AS avg_review_score
FROM car_data car
JOIN consumer_data cd ON car.model = cd.model
GROUP BY car.engine_type;

