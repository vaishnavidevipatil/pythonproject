# app.py
import mysql.connector
import pandas as pd
from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)

