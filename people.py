# from datetime import datetime
# from flask import abort
# from flask import abort, make_response
# import connexion

# app = connexion.App(__name__, specification_dir="./static")
# app.add_api("swagger.yml")

# # Flask app instance (for CORS, debug, etc.)
# application = app.app

# def get_timestamp():
#     return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# PEOPLE = {
#     "Fairy": {
#         "fname": "Tooth",
#         "lname": "Fairy",
#         "timestamp": get_timestamp(),
#     },
#     "Ruprecht": {
#         "fname": "Knecht",
#         "lname": "Ruprecht",
#         "timestamp": get_timestamp(),
#     },
#     "Bunny": {
#         "fname": "Easter",
#         "lname": "Bunny",
#         "timestamp": get_timestamp(),
#     }
# }

# def read_all():
#     return list(PEOPLE.values())

# def create(person):
#     lname = person.get("lname")
#     fname = person.get("fname", "")

#     if lname and lname not in PEOPLE:
#         PEOPLE[lname] = {
#             "lname": lname,
#             "fname": fname,
#             "timestamp": get_timestamp(),
#         }
#         return PEOPLE[lname], 201
#     else:
#         abort(
#             406,
#             f"Person with last name {lname} already exists",
#         )

# def read_one(lname):
#     if lname in PEOPLE:
#         return PEOPLE[lname]
#     else:
#         abort(
#             404, f"Person with last name {lname} not found"
#         )

# def update(lname, person):
#     if lname in PEOPLE:
#         PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
#         PEOPLE[lname]["timestamp"] = get_timestamp()
#         return PEOPLE[lname]
#     else:
#         abort(
#             404,
#             f"Person with last name {lname} not found"
#         )

# def delete(lname):
#     if lname in PEOPLE:
#         del PEOPLE[lname]
#         return make_response(
#             f"{lname} successfully deleted", 200
#         )
#     else:
#         abort(
#             404,
#             f"Person with last name {lname} not found"
#         )



# if __name__ == "__main__":
#     application.run(debug=True)

import redis
import json
from datetime import datetime
from flask import abort, make_response

# Redis connection (decode_responses=True for Python strings)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize sample data on first run (optional)
def init_sample_data():
    sample_people = {
        "Fairy": {"fname": "Tooth", "lname": "Fairy", "timestamp": get_timestamp()},
        "Ruprecht": {"fname": "Knecht", "lname": "Ruprecht", "timestamp": get_timestamp()},
        "Bunny": {"fname": "Easter", "lname": "Bunny", "timestamp": get_timestamp()}
    }
    for lname, data in sample_people.items():
        if not r.exists(f"person:{lname}"):
            r.hset(f"person:{lname}", mapping=data)

def read_all():
    people = []
    keys = r.scan_iter(match="person:*")
    for key in keys:
        data = r.hgetall(key)
        people.append(data)
    return people


def create(person=None, **kwargs):
    # Connexion sometimes passes the JSON inside kwargs['body']
    if person is None and 'body' in kwargs:
        person = kwargs['body']

    if not person:
        abort(400, "Last name is required in the request body")

    lname = person.get("lname")
    fname = person.get("fname", "")

    if not lname:
        abort(400, "Last name is required")

    person_key = f"person:{lname}"
    if r.exists(person_key):
        abort(406, f"Person with last name {lname} already exists")

    person_data = {
        "fname": fname,
        "lname": lname,
        "timestamp": get_timestamp()
    }
    r.hset(person_key, mapping=person_data)
    return person_data, 201


# def create(person):
#     lname = person.get("lname")
#     fname = person.get("fname", "")
    
#     if not lname:
#         abort(400, "Last name is required")
    
#     person_key = f"person:{lname}"
#     if r.exists(person_key):
#         abort(406, f"Person with last name {lname} already exists")
    
#     person_data = {
#         "fname": fname,
#         "lname": lname,
#         "timestamp": get_timestamp()
#     }
#     r.hset(person_key, mapping=person_data)
#     return person_data, 201

def read_one(lname):
    person_key = f"person:{lname}"
    if r.exists(person_key):
        return r.hgetall(person_key)
    abort(404, f"Person with last name {lname} not found")

# def update(lname, person):
#     person_key = f"person:{lname}"
#     if not r.exists(person_key):
#         abort(404, f"Person with last name {lname} not found")
    
#     # Update fname if provided, otherwise keep existing
#     if "fname" in person:
#         r.hset(person_key, "fname", person["fname"])
#     r.hset(person_key, "timestamp", get_timestamp())
    
#     return r.hgetall(person_key)

def update(lname, person=None, **kwargs):
    # Connexion sometimes passes the JSON inside kwargs['body']
    if person is None and 'body' in kwargs:
        person = kwargs['body']

    if not person:
        abort(400, "Request body required to update person")

    person_key = f"person:{lname}"
    if not r.exists(person_key):
        abort(404, f"Person with last name {lname} not found")

    # Update fname if provided
    if "fname" in person:
        r.hset(person_key, "fname", person["fname"])
    r.hset(person_key, "timestamp", get_timestamp())

    return r.hgetall(person_key)


def delete(lname):
    person_key = f"person:{lname}"
    if r.exists(person_key):
        r.delete(person_key)
        return make_response(f"{lname} deleted", 200)
    abort(404, f"Person with last name {lname} not found")
