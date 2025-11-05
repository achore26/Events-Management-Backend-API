from flask import Flask, request , jsonify
import mysql.connector
from dotenv import load_dotenv

app = Flask(__name__)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


cursor = conn.cursor()

@app.route('/register', methods=['POST','GET'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

   
    add_user = "INSERT INTO user (username, email, password, role) VALUES (%s, %s, %s, %s)"
    cursor.execute(add_user, (username, email, password, role))
    conn.commit()
 
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = conn.cursor()
    check_user = "SELECT * FROM user WHERE username = %s AND password = %s"
    cursor.execute(check_user, (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Accepted', 'role': user['role']}), 200
    else:
        return jsonify({'message': 'error'}), 401

@app.route('/<role>/events', methods=['GET'])
def list_events(role):
    cursor = conn.cursor()

    if role == 'organizer':
        query = "SELECT * FROM event"
        cursor.execute(query)
        events = cursor.fetchall()
        return jsonify({'events': events}), 200
    
    elif role == 'attendee':
        query = "SELECT id, event_name, location, date FROM event"
        cursor.execute(query)
        events = cursor.fetchall()
        return jsonify({'available_events': events}), 200


@app.route('/rsvp', methods=['POST'])
def rsvp():
    cursor = conn.cursor()

    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    rsvp = "INSERT INTO rsvp (user_id, event_id) VALUES (%s, %s)"
    cursor.execute(rsvp, (user_id, event_id))
    conn.commit()

    return jsonify({'message': 'confirmed attendance'}), 201

@app.route('/approve', methods=['POST'])
def approve():
    cursor = conn.cursor()
    data = request.get_json()
    rsvp_id = data.get('rsvp_id')
    status = data.get('status')

    update_status = "UPDATE rsvp SET status = %s WHERE id = %s"
    cursor.execute(update_status, (status, rsvp_id))
    conn.commit()

    return jsonify({'message': 'RSVP updated'}), 200

if __name__ == '__main__':
    app.run (debug=True)