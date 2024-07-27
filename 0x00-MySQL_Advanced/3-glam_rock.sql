-- Import the table dump
-- Assuming the table name is `bands` and it has columns `band_name`, `main_style`, `formed`, `split`
-- Please adjust the table name and column names if they differ

-- Step 1: Import the table dump
-- You need to unzip the provided file and load it into your database. The method to do this can vary based on your database system.
-- For example, in MySQL, you might use:
-- mysql -u username -p database_name < metal_bands.sql

--  lists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name AS band_name, IFNULL(split, 2020) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;