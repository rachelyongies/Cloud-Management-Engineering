import random
import string

from os import environ
from passlib.hash import sha256_crypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
db.create_all()

CORS(app)


class User_Detail(db.Model):
    __tablename__ = 'user_detail'

    user_type = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.String(15), primary_key=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(11))
    addresses = db.relationship(
        'User_Addresses', backref='user_detail'
    )

    def __init__(self, user_type, user_id, user_password, fullname, email, phone_number):
        self.user_type = user_type
        self.user_id = user_id
        self.user_password = user_password
        self.fullname = fullname
        self.email = email
        self.phone_number = phone_number

    def json(self):
        return({
            "user_type": self.user_type,
            "user_id": self.user_id,
            "user_password": self.user_password,
            "fullname": self.fullname,
            "email": self.email,
            "phone_number": self.phone_number
        })

class User_Addresses(db.Model):
    __tablename__ = 'user_addresses'

    user_id = db.Column(db.String(15), db.ForeignKey(
        'user_detail.user_id'), primary_key=True, nullable=False)
    postal_code = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(50), primary_key=True, nullable=False)
    user_address = db.Column(db.String(50))
    country = db.Column(db.String(50))

    def __init__(self, user_id, postal_code, city, user_address, country):
        self.user_id = user_id
        self.postal_code = postal_code
        self.city = city
        self.user_address = user_address
        self.country = country

    def json(self):
        return({
            "user_id": self.user_id,
            "postal_code": self.postal_code,
            "city": self.city,
            "user_address": self.user_address,
            "country": self.country
        })

    def print_json(self):
        print({
            "user_id": self.user_id,
            "postal_code": self.postal_code,
            "city": self.city,
            "user_address": self.user_address,
            "country": self.country
        })


db.create_all()


@app.route("/user/signup/<string:user_type>", methods=['POST'])
def signup(user_type):
    data = request.get_json()

    # Email Check
    user_row = User_Detail.query.filter_by(email=data["email"]).first()

    if user_row is not None:
        return jsonify(
            {
                "code": 400,
                "message": "That email has already been taken. Please Login or Register with a different email."
            }
        ), 400

    # Generating user_id
    user_id = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(15)])
    while (User_Detail.query.filter_by(user_id=user_id).first()):
        user_id = ''.join(
            [random.choice(string.ascii_letters + string.digits) for n in range(15)])

    # Password Hash
    data["user_password"] = sha256_crypt.hash(data["user_password"])

    user_object = User_Detail(user_type, user_id, **data)

    try:
        db.session.add(user_object)
        db.session.commit()
    except:
        name = 'User Signup'
        message = f"Error when creating the {user_type} user with email={data['email']}"

        return jsonify(
            {
                "code": 500,
                "message": "There was an issue with registration. Please try again."
            }
        ), 500

    name = 'User Signup'
    message = f"Successful creation of the {user_type} user with email={data['email']} and user_id={user_id}"

    return jsonify(
        {
            "code": 201,
            "message": "Registration Successful"
        }
    ), 201


@app.route("/user/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["user_password"]

    # Retrieve User row from db
    user_row = User_Detail.query.filter_by(email=email).first()

    if user_row is not None:
        db_password = user_row.user_password

        # Password Verify
        verified = sha256_crypt.verify(password, db_password)

        if verified:
            return jsonify({
                "code": 200,
                "user_type": user_row.user_type,
                "user_details": {
                    "user_id": user_row.user_id,
                    "email": user_row.email,
                    "fullname": user_row.fullname,
                    "phone_number": user_row.phone_number,
                }
            }), 200

    return jsonify({
        "code": 401,
        "message": "Authentication Failed. The email and/or password provided is incorrect"
    }), 401


@app.route("/user/<string:user_id>/addresses")
def get_user_addresses(user_id):
    user_addresses = User_Addresses.query.filter_by(user_id=user_id)
    if user_addresses is not None:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "addresses": [address.json() for address in user_addresses]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no addresses."
        }
    ), 404

@app.route("/user/<string:user_id>/addresses/add_address", methods=['POST'])
def add_user_address(user_id):
    data = request.get_json()
    city = data["city"]
    postal_code = data["postal_code"]
    user_address = data["user_address"]
    country = data['country']

    if(User_Addresses.query.filter_by(user_id=user_id, city=city, postal_code=postal_code, country=country).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "address": user_address
                },
                "message": "Address already exists."
            }
        ), 400

    new_row = User_Addresses(user_id, **data)

    try:
        db.session.add(new_row)
        db.session.commit()
    except:
        name = 'User Add Address'
        message = f"Error during addition of address for the user {user_id}"

        return jsonify(
            {
                "code": 500,
                "message": "There was an issue with addition of address. Please try again."
            }
        )

    name = 'User Add Address'
    message = f"Successful addition of credit card for the user {user_id}"

    return jsonify(
        {
            "code": 201,
            "message": "Addition of address Successful"
        }
    )


@app.route("/user/details/<string:user_id>")
def get_details(user_id):
    try:
        user_row = User_Detail.query.filter_by(user_id=user_id).first()

        if user_row.user_type == 'admin':
            return jsonify({
                "code": 400,
                "message": "Please provide a user_id belonging to a user, instead of an admin"
            }), 400
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong with the retrieval of user data"
        }), 500
    return jsonify({
        "code": 200,
        "details": user_row.json()
    }), 200

@app.route("/user/email_list", methods=['POST'])
def get_email_list():
    data = request.get_json()
    user_list = data['user_list']

    try:
        email_rows = User_Detail.query.filter(User_Detail.user_id.in_(user_list)).all()
    except:
        return jsonify({
            "code": 400,
            "message": "Error when retrieving email_list. Please provide a valid user_list."
        }), 400
    email_list = []

    for row in email_rows:
        if row.email not in email_list:
            email_list.append(row.email)

    if len(email_list):
        return jsonify({
            "code": 200,
            "email_list": email_list
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
