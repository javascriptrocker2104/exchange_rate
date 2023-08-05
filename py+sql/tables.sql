CREATE TABLE IF NOT exists rate 
(id serial PRIMARY KEY,
rate_date DATE,
rate_amount DECIMAL);

CREATE TABLE IF NOT exists rates_per_month 
(id serial PRIMARY KEY,
start_date DATE,
end_date DATE,
max_date DATE,
min_date DATE,
max_amount DECIMAL,
min_amount DECIMAL,
avg_amount DECIMAL,
last_date_amount DECIMAL);

--select * from rates_per_month