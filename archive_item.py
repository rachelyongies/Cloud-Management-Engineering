import os
import requests

from amqp_invoke import notification_invoke
from os import environ
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

item_URL = os.environ.get('item_URL')
order_URL = os.environ.get('order_URL')
user_URL = os.environ.get('user_URL')
 
@app.route('/archive_item', methods=['PUT'])
def archive_item():
    # 1 Change item status
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

    # 2 Notify Users

    # 2.1 Find all orders with this item
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

    # 2.2 Find all related emails
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

    # 2.3 Invoke Notification
    email_type = 'archive_order'
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
    app.run(host='0.0.0.0', port=5222, debug=True)

