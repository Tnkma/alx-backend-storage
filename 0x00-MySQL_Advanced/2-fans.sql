-- Assuming the metal_bands table is already created and populated
-- The following SQL script ranks countries by the number of fans

SELECT origin,
       SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
