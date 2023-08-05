import requests
import psycopg2
from psycopg2 import sql

#курс за июнь 2023
url = 'https://api.exchangerate.host/timeseries?start_date=2023-06-01&end_date=2023-06-30&base=BTC&symbols=RUB'
response = requests.get(url)
data = response.json()

#созданием словари
lst = []
for i in data['rates']:
    for j in data['rates'][i]:
        lst.append((i, data['rates'][i][j]))

#устанавливаем соединение
conn = psycopg2.connect(dbname='database', 
                              user='anne', 
                              password='get_rate', 
                              host='localhost',
                              port=5432)

with conn.cursor() as cursor:
    conn.autocommit = True
    #загрузка словарей в бд PostgresSQL
    insert = sql.SQL('INSERT INTO rate (rate_date, rate_amount) VALUES {}').format(sql.SQL(',').join(map(sql.Literal, lst)))
    cursor.execute(insert)

    res = []

    cursor.execute('SELECT * FROM rate')
    max_amount = 0
    min_amount = 0
    avg_amount = 0
    i = 0 #счетчик для avg
    for row in cursor:
        i += 1
        if row[2] > max_amount:
            max_date = row[1]
            max_amount = row[2]
        elif min_amount == 0 or row[2] < min_amount:
            min_amount = row[2]
            min_date = row[1]
            avg_amount = avg_amount + row[2]
            last_date_amount = row[2]
    avg_amount = avg_amount / i

    res.append((data['start_date'],data['end_date'], max_date, min_date, max_amount, min_amount, avg_amount, last_date_amount))

    insert = sql.SQL('INSERT INTO rates_per_month (start_date,end_date, max_date, min_date, max_amount, min_amount, avg_amount, last_date_amount) VALUES {}').format(sql.SQL(',').join(map(sql.Literal, res)))
    cursor.execute(insert)
conn.commit()
#закрываем соединение
conn.close()