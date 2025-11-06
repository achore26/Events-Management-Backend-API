Hello Welcome to this test project

lets get you setup....
clone repository 
    "git clone https://github.com/achore26/Events-Management-Backend-API"

create a virtual environment
    python3 -m venv venv 
    source venv/bin/activate

Install dependencies
    pip install flask mysql-connector-python python-dotenv flasgger flask-swagger-ui

setup the sql database
with the following tables 
user
    CREATE TABLE user CREATE TABLE user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50 NOT NULL,
        password VARCHAR(50),
        role ENUM('organizer','attendee')
    );
rsvp,
  CREATE TABLE user CREATE TABLE rsvp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        event_id INT NOT NULL,
        status ENUM('accepted','rejected'),
        FOREIGN KEY (user_id) REFERENCES user(id)
        FOREIGN KEY (event_id) REFERENCES event(id)
    );

event
      CREATE TABLE user CREATE TABLE event (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_name VARCHAR(50) NOT NULL,
        location VARCHAR(50) NOT NULL,
        date DATETIME,
        maximum_attendance INT NOT NULL,
        organizer_id INT,
        FOREIGN KEY organiser_id REFERENCES user(id)
    );


run the application 
    python3 app.py

API Endpoints
    go to: localhost:5000/apidocs to see the api documentation.
