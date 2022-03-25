import os
import requests

from amqp_invoke import notification_invoke
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

item_URL = os.environ.get('item_URL')
order_URL = os.environ.get('order_URL')
user_URL = os.environ.get('user_URL')

@app.route('/fulfill_order', methods=['PUT'])
def fulfill_order():

    # 1 Notify external API to handle shipping
    # Here is where we will contact our external API for shipping
    # some code for connecting to external API...

    # 2 Change status of item
    data = request.get_json()
    item_id = data["item_id"]

    method = 'PUT'
    url = f'{item_URL}/{item_id}'

    r = requests.request(method, url)

    if r.status_code != 200:
        return jsonify(
            {
                "code": 500,
                "message": "Internal communication error."
            }
        ), 500

    item_name = r.json()['item_name']

    # 3 Notify Users
    # 3.1 Find all orders with this item
    method = 'GET'
    url = f'{order_URL}/{item_id}'

    response = requests.request(method, url)

    if r.status_code != 200:
        return jsonify(
            {
                "code": 500,
                "message": "Internal communication error."
            }
        ), 500

    user_list = response.json()['user_list']

    # 3.2 Find all related emails
    method = 'POST'
    url = user_URL
    json = { "user_list": user_list}

    response = requests.request(method, url, json=json)

    if r.status_code != 200:
        return jsonify(
            {
                "code": 500,
                "message": "Internal communication error."
            }
        ), 500

    email_list = response.json()['email_list']

    # 3.3 Invoke Notification
    email_type = 'fulfill_order'
    message_details = {
        "item_name": item_name
    }

    notification_invoke(email_type=email_type, email_list=email_list, message_details=message_details)

    return jsonify(
        {
            "code": 200,
            "message": "Status update to archive has been a success"
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
