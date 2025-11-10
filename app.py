from flask import Flask, request , jsonify
import mysql.connector, os
from dotenv import load_dotenv
from flasgger import Swagger
import jwt
import datetime

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

def verify_token():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"Error" : "There is no token detected"}),403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['username']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": 'Token expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({"messsage" : "Invalid Token"}), 401


@app.route('/register', methods=['POST','GET'])
def register():
    """
        This is an example endpoint that registers a user as either an organizer or an attendee.
        ---
        tags:
            - Registration
        description: gets a users details from the front end, parses them in json formart and stores them in the database
        responses:
            201:
                description: A successful input
                examples:
                    application/json: "User registered successfully"
    """
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')

    
        add_user = "INSERT INTO user (username, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(add_user, (username, email, password, role))
        conn.commit()
    
        return jsonify({'message': 'User registered successfully'}), 201
    
    return jsonify({"Message" : "This is the registration page."})


@app.route('/login', methods=['POST','GET'])
def login():
    """
        This is an example endpoint that logs in  a user.
        ---
        tags:
            - Login
        description: gets a users details from the front end, parses them in json formart and stores them in the database
        responses:
            200:
                description: accepted the details 
                examples:
                    application/json: "User loged in successfully
            401:
                description: error in details"
                examples:
                    application/json: "Invalid username or password"
    """
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        cursor = conn.cursor()
        check_user = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(check_user, (username, password))
        user = cursor.fetchone()

        if user:
            Token = encoded_jwt = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes =2)}, app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({'message': 'Accepted', 'role': user['role']}), 200
        else:
            return jsonify({'message': 'error, this user may not exist'}), 401
        
    return jsonify({"Message" : "Hello, This is the login page"})

@app.route('/<role>/events', methods=['GET'])
def list_events(role):

    """
        This is an example endpoint that lists the events present in the database.
        ---
        tags:
            - events
        description: list the events based on user role
        responses:
            200:
                description: Users events listed successfully
                examples:
                    application/json: "tennis event"
    """
 
    verify_token()
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


@app.route('/rsvp', methods=['POST','GET'])
def rsvp():
    """
        This is an example endpoint that rsvp's the attendee's.
        ---
        tags:
            - Registration
        description: gets a users details from the front end, parses them in json formart and stores them in the database
        responses:
            201:
                description: A successful input
                examples:
                    application/json: "attendance Confirmed"
    """
    if request.method == 'POST':
        verify_token()
        cursor = conn.cursor()

        data = request.get_json()
        user_id = data.get('user_id')
        event_id = data.get('event_id')

        rsvp = "INSERT INTO rsvp (user_id, event_id) VALUES (%s, %s)"
        cursor.execute(rsvp, (user_id, event_id))
        conn.commit()

        return jsonify({'message': 'confirmed attendance'}), 201
    
    return jsonify({"Message" : "You have reached the rsvp's page "}),200


@app.route('/approve', methods=['POST','GET'])
def approve():
        """
            This is an example endpoint that approves or rejects the rsvp's.
            ---
            tags:
                - Approval
            description: gets a users details from the front end, converts them to json formart and updates them in the database
            responses:
                200:
                    description: A successful update
                    examples:
                        application/json: "RSVP updated"
        """
        
        if request.method == 'POST': 
            verify_token()

            cursor = conn.cursor()
            data = request.get_json()
            rsvp_id = data.get('rsvp_id')
            status = data.get('status')

            update_status = "UPDATE rsvp SET status = %s WHERE id = %s"
            cursor.execute(update_status, (status, rsvp_id))
            conn.commit()

            return jsonify({'message': 'RSVP updated'}), 200
        
        return jsonify({"Message" : "This is the approved page"}),200

if __name__ == '__main__':
    app.run (debug=True)