from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/assignment_submission"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Get your collections
users_collection = mongo.db.users  # Users collection
assignments_collection = mongo.db.assignments  # Assignments collection
admins_collection = mongo.db.admins  # Admins collection (use a separate collection for admins)

@app.route('/')
def index():
    return "Welcome to the Assignment Submission Portal!"

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Save user to the database
    users_collection.insert_one({'username': username, 'password': hashed_password})

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    user = users_collection.find_one({'username': username})

    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials!"}), 401

@app.route('/upload', methods=['POST'])
def upload_assignment():
    user_id = session.get('user_id')  # Get the user ID from the session
    if not user_id:
        return jsonify({"error": "User not logged in!"}), 401

    task = request.json.get('task')
    admin = request.json.get('admin')

    if not task or not admin:
        return jsonify({"error": "Task and admin fields are required!"}), 400

    # Create the assignment object
    assignment = {
        'userId': user_id,
        'task': task,
        'admin': admin
    }

    # Save the assignment to the database
    assignments_collection.insert_one(assignment)

    return jsonify({"message": "Assignment uploaded successfully!"}), 201

@app.route('/assignments', methods=['GET'])
def view_assignments():
    admin_id = session.get('user_id')  # Get the admin ID from the session
    if not admin_id:
        return jsonify({"error": "Admin not logged in!"}), 401

    # Fetch assignments tagged to the admin
    assignments = assignments_collection.find({'admin': admin_id})
    
    # Convert assignments to a list
    assignments_list = []
    for assignment in assignments:
        assignment['_id'] = str(assignment['_id'])  # Convert ObjectId to string
        assignments_list.append(assignment)

    return jsonify(assignments_list), 200

@app.route('/admin/register', methods=['POST'])
def admin_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if admins_collection.find_one({"username": username}):
        return jsonify({"error": "Admin username already exists!"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Insert new admin user into the collection
    admins_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "Admin registered successfully!"}), 201

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json  # Use request.json instead of request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = admins_collection.find_one({"username": username})

    if not admin or not check_password_hash(admin['password'], password):
        return jsonify({"error": "Invalid credentials!"}), 401

    session['username'] = username
    return jsonify({"message": "Admin login successful!"})

@app.route('/admin/assignments', methods=['GET'])
def admin_view_assignments():
    if 'username' not in session:
        return jsonify({"error": "Admin not logged in!"}), 401

    # Find assignments tagged to the logged-in admin
    assignments = list(assignments_collection.find({"admin": session['username']}))

    # Remove MongoDB specific '_id' field for serialization
    for assignment in assignments:
        assignment['_id'] = str(assignment['_id'])

    return jsonify(assignments)

@app.route('/admin/assignments/<assignment_id>/accept', methods=['POST'])
def accept_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({"error": "Admin not logged in!"}), 401

    # Validate ObjectId
    if not ObjectId.is_valid(assignment_id):
        return jsonify({"error": "Invalid assignment ID!"}), 400

    result = assignments_collection.update_one({"_id": ObjectId(assignment_id)}, {"$set": {"status": "accepted"}})
    
    if result.modified_count == 0:
        return jsonify({"error": "Assignment not found or status already accepted!"}), 404

    return jsonify({"message": "Assignment accepted!"})

@app.route('/admin/assignments/<assignment_id>/reject', methods=['POST'])
def reject_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({"error": "Admin not logged in!"}), 401

    # Validate ObjectId
    if not ObjectId.is_valid(assignment_id):
        return jsonify({"error": "Invalid assignment ID!"}), 400

    result = assignments_collection.update_one({"_id": ObjectId(assignment_id)}, {"$set": {"status": "rejected"}})
    
    if result.modified_count == 0:
        return jsonify({"error": "Assignment not found or status already rejected!"}), 404

    return jsonify({"message": "Assignment rejected!"})

if __name__ == '__main__':
    app.run(debug=True)
