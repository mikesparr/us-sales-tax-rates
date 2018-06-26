
DROP DATABASE tax_rates;
CREATE DATABASE tax_rates;
USE tax_rates;

CREATE TABLE rate (zip_code INT(5) NOT NULL, state VARCHAR(2) NOT NULL, tax_region_name VARCHAR(255) NULL, state_rate DECIMAL(12,6), est_combined_rate DECIMAL(12,6), est_county_rate DECIMAL(12,6), est_city_rate DECIMAL(12,6), est_special_rate DECIMAL(12,6), risk_level TINYINT(1), PRIMARY KEY (zip_code));

DROP USER IF EXISTS 'user_tax'@'%';
CREATE USER 'user_tax'@'%' IDENTIFIED BY 'unclesam';
GRANT ALL PRIVILEGES ON tax_rates.* TO 'user_tax'@'%';
FLUSH PRIVILEGES;
