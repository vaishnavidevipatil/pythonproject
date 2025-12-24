# main app of flask runs on RESTful API to Student data
import mysql.connector
import pandas as pd
from flask import Flask,request, jsonify
app = Flask(__name__)

@app.route('/api/get/students/data', methods=['GET'])
def get_data():
    # Create a connection object
    my_conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mysqltut")
    
    df = pd.read_sql("SELECT * FROM mysqltut.students",con= my_conn)
    my_conn.close()
    # Replace this with the actual data you want to return
    data=df.to_dict("records")
    return jsonify(data)

@app.route('/api/add/student', methods=['POST'])
def add_student():
    try:
        # Create a connection object
        my_conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mysqltut")
    
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

# Put method to update student data
@app.route('/update/students/data/<int:id>', methods=['PUT'])
def update_data(id):
    try:
        # Parse JSON body
        data = request.get_json()

        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400

        print(">>>>>data", data)

        # Connect to MySQL
        my_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mysqltut"
        )
        cursor = my_conn.cursor()

        # Correct SQL update query
        update_query = """
            UPDATE students
            SET name = %s,
                age = %s,
                course = %s
            WHERE id = %s
        """

        # Execute query with all values
        cursor.execute(update_query, (
            data["name"],
            data["age"],
            data["course"],
            id
        ))

        my_conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                'status': 'warning',
                'message': f'No student found with id {id}'
            }), 404

        return jsonify({
            'status': 'success',
            'message': 'Data updated successfully',
            'updated_id': id,
            'updated_fields': data
        })
    except Exception as e:
        print("ERROR>>>>>>>>>>:", e)   # <-- Very important for debugging
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        try:
            cursor.close()
            my_conn.close()
        except:
            pass


@app.route('/delete/students/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        # Connect to DB
        my_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mysqltut"
        )
        cursor = my_conn.cursor()

        # Delete query
        delete_query = "DELETE FROM students WHERE id = %s"

        cursor.execute(delete_query, (id,))
        my_conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                'status': 'error',
                'message': f'No record found with id {id}'
            }), 404

        return jsonify({
            'status': 'success',
            'message': f'Student with id {id} deleted successfully'
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        try:
            cursor.close()
            my_conn.close()
        except:
            pass


if __name__ == '__main__':
    app.run(debug=True)
