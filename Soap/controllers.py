import json
import uuid
from model import User

# File to store user data
DATA_FILE = 'users.json'

# Load users from JSON file


def load_users():
    try:
        with open("users.json") as f:
            USERS = json.load(f)
    except:
        USERS = {}

# Save users to JSON file


def save_users(users):
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def add_user(name, email, description):
    users = load_users()
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "description": description
    }
    save_users(users)
    return user_id


def get_user(user_id):
    users = load_users()
    return users.get(user_id)


def update_user(user_id, name, email, description):
    users = load_users()
    if user_id in users:
        users[user_id] = {
            "id": user_id,
            "name": name,
            "email": email,
            "description": description
        }
        save_users(users)
        return True
    return False


def delete_user(user_id):
    users = load_users()
    if user_id in users:
        del users[user_id]
        save_users(users)
        return True
    return False


def list_users():
    return list(load_users().values())