from flask import *
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user-api'
mongo = PyMongo(app)

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'error': 'User already exists'}), 400

    mongo.db.users.insert_one({'email': email, 'password': password})

    return jsonify({'message': 'User created successfully'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({'email': email})
    if not user or not user['password'] == password:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

# Manage users
@app.route('/profile/<string:email>', methods=['GET'])
def get_profile(email):
    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Convert ObjectId to string before returning JSON
    user['_id'] = str(user['_id'])
    return jsonify({"User": user})

@app.route('/profile/<string:email>', methods=['PUT'])
def update_profile(email):
    data = request.json
    new_email = data.get('email')
    new_password = data.get('password')

    if not new_email or not new_password:
        return jsonify({'error': 'Email and password is required for update'}), 400

    update_fields = {}
    if new_email:
        update_fields['email'] = new_email
    if new_password:
        update_fields['password'] = new_password

    result = mongo.db.users.update_one({'email': email}, {'$set': update_fields})
    if result.modified_count == 0:
        return jsonify({'error': 'Please enter a valid values'}), 404

    return jsonify({'message': 'Profile updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
