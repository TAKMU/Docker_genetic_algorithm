#Program made by Allan Miyazono for company Microflow S.A. de C.V.


from flask import (
    Flask, render_template, request, make_response
)
import os
from flask_cors import CORS
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import db_access
import sistemas_inteligentes 

load_dotenv()

app = Flask(__name__, instance_relative_config=True,
            static_folder="./templates/static", template_folder="./templates")
app.config['SECRET_KEY'] = '12345'
app.config['API_KEY'] = 'api_key'

cors = CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    return render_template('index.html')

 # region Validate

@app.route('/api/solve', methods=(['GET']))
def get_solution():
    try:
        combination, score =sistemas_inteligentes.solution()
        data = {"combination": combination,
                "score": score}
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response


@app.route('/api/get-variables', methods=(['GET']))
def get_variables():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM variables")
        var_ai = cur.fetchone()
        cur.close()
        conn.close()
        data = {
            "id": int(var_ai[0]),
            "n_pop": int(var_ai[1]),
            "n_generations": int(var_ai[2]), 
            "p_selection": float(var_ai[3]),
            "p_mutate" : float(var_ai[4]),
            "max_value": int(var_ai[5]),
            "min_value": int(var_ai[6]),
            "max_weight": float(var_ai[7]),
            "budget": int(var_ai[8])                    
            }
        print(data)
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

@app.route('/api/put-variables', methods=(['PUT']))
def put_variables():
    try:
        request_data = request.get_json()
        n_pop = request_data['n_pop']
        n_generations = request_data['n_generations']
        p_selection = request_data['p_selection']
        p_mutate = request_data['p_mutate']
        min_value = request_data['min_value']
        max_value = request_data['max_value']
        budget = request_data['budget']
        max_weight = request_data['max_weight']
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute('UPDATE variables '
            'SET n_pop =%s, ' 
            'n_generations = %s, ' 
            'p_selection = %s, ' 
            'p_mutate = %s, '
            'max_value = %s, '
            'min_value = %s, '
            'max_weight = %s, '
            'budget = %s '
            'WHERE id = 1',
            (n_pop,
             n_generations,
             p_selection,
             p_mutate,
             max_value,
             min_value,
             max_weight,
             budget)
            )
        conn.commit()
        cur.close()
        conn.close()

        data = {'Message': "Se realizó el cambio con éxito."}
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

@app.route('/api/get-products', methods=(['GET']))
def get_products():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        sql_query = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM products
                               ''', conn)
        data = pd.DataFrame(sql_query, columns = ['id', 'product_name', 'weight', 'buy_price', 'sale_price'])
        print(data)
        data = data.to_json(orient="records")
        print(data)
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

@app.route('/api/get-product/<int:id>', methods=(['GET']))
def get_product(id):
    try:
        print(id)
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE id = %s", str(id))
        var_ai = cur.fetchone()
        cur.close()
        conn.close()
        data = {"product_name": var_ai[1],
                "weight": float(var_ai[2]), 
                "buy_price": float(var_ai[3]),
                "sale_price" : float(var_ai[4])
                }
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

@app.route('/api/post-products', methods=(['POST']))
def post_product():
    try:
        request_data = request.get_json()
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute('INSERT INTO products (product_name, weight, buy_price, sale_price)'
            'VALUES (%s, %s, %s, %s)',
            (request_data['product_name'],
             request_data['weight'],
             request_data['buy_price'],
             request_data['sale_price'])
            )
        cur.close()
        conn.commit()
        conn.close()
        data = {'Message': "Se realizó el cambio con éxito."}
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

            

@app.route('/api/delete-product/<int:id>', methods=(['DELETE']))
def delete_product(id):
    try:
        print(id)
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute("DELETE FROM Products WHERE id = %s", str(id))
        cur.close()
        conn.commit()
        conn.close()
        data = {'Message': "Se realizó el cambio con éxito."}
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response


@app.route('/api/put-products/<int:rowid>', methods=(['PUT']))
def put_products(rowid):
    try:
        request_data = request.get_json()
        print(request_data)
        id_product = rowid
        product_name = request_data['product_name']
        weight = request_data['weight']
        sale_price = request_data['sale_price']
        buy_price = request_data['buy_price']
        
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute('UPDATE products '
            'SET product_name =%s, ' 
            'weight = %s, ' 
            'buy_price = %s, ' 
            'sale_price = %s '
            'WHERE id = %s',
            (product_name,
             weight,
             buy_price,
             sale_price,
             id_product)
            )
        conn.commit()
        cur.close()
        conn.close()
        data = {'Message': "Se realizó el cambio con éxito."}
        response = make_response(data, 200)
        return response
        
    except Exception as e:
            print(e)
            data = {"Message": f"Error: {e}", 
                    "Severity": 'error'}
            response = make_response(data, 400)
            return response

app.run(debug=True, host='0.0.0.0')
    # endregion



