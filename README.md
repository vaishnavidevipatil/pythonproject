# pythonproject
python Restful project flask mysql 

📘 README — Python RESTful Project (Flask + MySQL)
🚀 Project Overview

This project is a simple RESTful CRUD API built using Flask and MySQL.
It provides a backend service to manage student data such as: Name, Age, Email, Course

The API supports Create, Read, Update, Delete operations with proper JSON responses and error handling.

🗄️ 1. MySQL Table Creation
Run the following SQL script to create the students table:
CREATE DATABASE IF NOT EXISTS mysqltut;

USE mysqltut;
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255),
    course VARCHAR(255)
);

🌐 2. CRUD API Endpoints
📌 Base URL: http://127.0.0.1:5000

📘 3. API Endpoints Table
➤ CREATE (POST)
Method Endpoint Description
POST:	/add/students/data	Add a new student record

JSON Body Example
{
  "name": "John Doe",
  "age": 22,
  "email": "john@example.com",
  "course": "Python Full Stack"
}

➤ READ (GET)
Method	Endpoint	Description
GET	/students	Get all students
GET	/students/<id>	Get student details by ID
➤ UPDATE (PUT)
Method	Endpoint	Description
PUT	/update/students/data/<id>	Update student by ID

JSON Body Example
{
  "name": "Vaishnavi Devi Patil",
  "age": 24,
  "email": "vaishnavip17@gmail.com",
  "course": "Python Full Stack"
}

➤ DELETE (DELETE)
Method	Endpoint	Description
DELETE	/delete/students/data/<id>	Delete student by ID
🛠️ 4. Project Setup Instructions
1️⃣ Install Dependencies
pip install flask mysql-connector-python

2️⃣ Run Flask Application
python app.py


_------------------------ People Module for Swagger app ------------------------_
# people.py
import connexion 
ui of the swagger : http://localhost:5000/ui/
the swagger helps to test api on the ui 
using redis key value pair

1. GET – Retrieve data

GET /people → read_all()

Redis: SCAN or KEYS to list all person:*
HGETALL to get each person's details
GET /people/{lname} → read_one(lname)
Redis: HGETALL person:{lname}
Purpose: Fetch data, no modifications.

2. POST – Create new data

POST /people → create(person)
Redis: EXISTS person:{lname} to check uniqueness
HSET person:{lname} {fname, lname, timestamp} to store new person
Purpose: Add new record. Fails if key already exists.

3. PUT – Update existing data

PUT /people/{lname} → update(lname, person)
Redis: EXISTS person:{lname} to ensure record exists
HSET person:{lname} fname=<new_value> to update fields
Update timestamp to mark modification
Purpose: Modify existing record. Can partially update fields.

4. DELETE – Remove data

DELETE /people/{lname} → delete(lname)
Redis: EXISTS person:{lname} to check if present
DEL person:{lname} to remove record
Purpose: Remove a record permanently.

Quick   Redis key/value mapping:
-----------------------------------------------
HTTP  _  Method	Redis   Operation	Notes
GET	  |  HGETALL / SCAN	| Read data
POST	|  HSET + EXISTS	| Create new key/value
PUT	  |  HSET + EXISTS	| Update fields of existing key
DELETE|	DEL + EXISTS	  | Remove key
