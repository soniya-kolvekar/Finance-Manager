import json
import os

DATA_FILE = "data.json"

def load_data():
    """Load data from data.json."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        
        # Initialize missing fields (such as "goals", "budget", "investments", "loans", and "debts")
        for username, user_data in data["users"].items():
            if "goals" not in user_data:
                user_data["goals"] = {}  # Initialize goals if not present
            if "budget" not in user_data:
                user_data["budget"] = {}  # Initialize budget if not present
            if "investments" not in user_data:
                user_data["investments"] = []  # Initialize investments if not present
            if "loans" not in user_data:
                user_data["loans"] = []  # Initialize loans if not present
            if "debts" not in user_data:
                user_data["debts"] = []  # Initialize debts if not present
        
        return data
    else:
        return {"users": {}}  # Return empty data structure if no file exists

def save_data(data):
    """Save data to data.json."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def register(username, password):
    """Register a new user."""
    data = load_data()

    # Check if username already exists
    if username in data["users"]:
        print("Username already exists!")
        return False

    # Add new user to data
    data["users"][username] = {
        "password": password,
        "income": [],
        "expenses": [],
        "balance": 0,
        "budget": {},
        "goals": {},
        "investments": [],  # Initialize investments field
        "loans": [],  # Initialize loans field
        "debts": []  # Initialize debts field
    }

    save_data(data)
    print("Registration successful!")
    return True

def authenticate(username, password):
    """Authenticate user during login."""
    data = load_data()

    if username in data["users"] and data["users"][username]["password"] == password:
        return True
    return False