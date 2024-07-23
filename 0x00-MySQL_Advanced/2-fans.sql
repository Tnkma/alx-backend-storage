-- Assuming the metal_bands table is already created and populated
-- The following SQL script ranks countries by the number of fans

SELECT origin,
       SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
