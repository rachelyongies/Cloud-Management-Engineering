from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
import pymysql

app = Flask(__name__)
CORS(app)

item_URL = os.environ.get('item_URL')
order_URL = os.environ.get('order_URL')
payment_URL = os.environ.get('payment_URL')
user_URL = os.environ.get('user_URL')

@app.route("/place_order", methods=['POST'])
def place_order():
    data = request.get_json()

    # 1. handle payment
    method = "POST"
    json = {}
    json['amount'] = data['amount']
    json['card_number'] = data['payment_details']['card_number']
    json['cvv'] = data['payment_details']['cvv']
    json['expiry_month'] = data['payment_details']['expiry_month']
    json['expiry_year'] = data['payment_details']['expiry_year']
    json['cardholder_name'] = data['payment_details']['cardholder_name']

    try:
        response = requests.request(method, payment_URL, json = json)
    except:
        return jsonify({
            "code": 500,
            "message": "Internal communication error."
        }), 500

    if response.status_code != 200:
        return response.json() ,response.status_code

    payment_amount = data['amount']

    # 2. send request to item microservice to increase the item_count by x amount
    method = "PUT"

    for item in data['items']:
        item_id = item['item_id']
        quantity = item['quantity']

        json = {
            "item_id": item_id,
            "quantity": quantity
        }

        try:
            response = requests.request(method, item_URL, json = json)
        except:
            return jsonify({
                "code":500,
                "message": "Internal communication error."
            }), 500

        if response.status_code != 200:
            return response.json() ,response.status_code

    item_list = data['items']

    # 3. send request to order microservice (creates an order)
    method = "POST"
    json = {
        "user_id": data['user_id'],
        "items": data['items']
    }

    try:
        response = requests.request(method, order_URL, json = json)
    
    except:
        return jsonify({
            "code":500,
            "message": "Internal communication error."
        }),500

    if response.status_code != 201:
        return response.json() ,response.status_code

    order_id = response.json()['order_id']

    # # 4. send notification
    # method = 'GET'
    # url = user_URL + f'/{data["user_id"]}'
    # response = requests.request(method, url)

    # email_type = 'place_order'
    # fullname = response.json()['details']['fullname']
    # email = response.json()['details']['email']
    # message_details = {
    #     "payment_amount": payment_amount,
    #     "order_id": order_id,
    #     "item_list": item_list
    # }

    # notification_invoke(email_type=email_type, fullname=fullname, email_list=[email], message_details=message_details)

    # If everything is oll korreck (ok)
    return jsonify({
        "code": 200,
        "message": 'Successfully placed order.'
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600, debug=True)
