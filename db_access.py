import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        #port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS products;')
cur.execute('CREATE TABLE products (id serial PRIMARY KEY,'
                                 'product_name varchar (150) NOT NULL,'
                                 'weight decimal NOT NULL,'
                                 'buy_price smallint NOT NULL,'
                                 'sale_price smallint NOT NULL);'
                                 )

cur.execute('DROP TABLE IF EXISTS variables;')
cur.execute('CREATE TABLE variables ('
                                 'id smallint NOT NULL,'
                                 'n_pop smallint NOT NULL,'
                                 'n_generations smallint NOT NULL,'
                                 'p_selection decimal NOT NULL,'
                                 'p_mutate decimal NOT NULL,'
                                 'max_value smallint NOT NULL,'
                                 'min_value smallint NOT NULL,'
                                 'max_weight decimal NOT NULL,'
                                 'budget smallint NOT NULL);'
                                 )

# Insert data into the table
cur.execute('INSERT INTO variables (id, n_pop, n_generations, p_mutate, p_selection, max_value, min_value, max_weight, budget)'
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (1,
             500,
             1000,
             .4,
             .7,
             7,
             1,
             15,
             1000
             )
            )


cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Dubalin',
             0.6,
             60,
             70)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Chocolate',
             0.5,
             30,
             80)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Sabritas',
             0.1,
             80,
             140)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Gansitos',
             0.6,
             66,
             100)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Bubaloo',
             2.0,
             34,
             170)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Panditas',
             0.2,
             76,
             76)
            )

cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            ('Kranky',
             0.3,
             33,
             124)
            )


conn.commit()

cur.close()
conn.close()
