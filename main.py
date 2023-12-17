# app.py
import mysql.connector
import pandas as pd
from flask import Flask,request, jsonify
app = Flask(__name__)

@app.route('/api/get/students/data', methods=['GET'])
def get_data():
    # Create a connection object
    my_conn = mysql.connector.connect(host="localhost", user="root", password="Mysql@2024", database="mysqltut")
    
    df = pd.read_sql("SELECT * FROM mysqltut.students",con= my_conn)
    my_conn.close()
    # Replace this with the actual data you want to return
    data=df.to_dict("records")
    return jsonify(data)

@app.route('/api/add/student', methods=['POST'])
def add_student():
    try:
        # Create a connection object
        my_conn = mysql.connector.connect(host="localhost", user="root", password="Mysql@2024", database="mysqltut")
    
        # Get data from the request
        data = request.get_json()

        # Convert data to a Pandas DataFrame
        df = pd.DataFrame([data])
        print(df)
        # Write data to the MySQL database
        cursor = my_conn.cursor()

        # Specify target table columns in the SQL statement
        columns = ', '.join(df.columns)
        values = ', '.join(['%s'] * len(df.columns))
        query = f"INSERT INTO students ({columns}) VALUES ({values})"
        
        cursor.executemany(query, df.values.tolist())
        my_conn.commit()

        return jsonify({'message': 'Student record added successfully'})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

    finally:
        # Close the database connection
        if 'connection' in locals() and my_conn.is_connected():
            my_conn.close()


if __name__ == '__main__':
    app.run(debug=True)

