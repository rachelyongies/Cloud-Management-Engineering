import requests

import json
import os

import amqp_setup

#for sending email
def send_simple_message(email_list, message):
    response = requests.post(
        "https://api.mailgun.net/v3/sandboxcea5052ebb6044f8a5886ff620c4efaf.mailgun.org/messages",
        auth=("api", "aeb37e3aa25b8a22fb7b7c6520b98fbc-b6d086a8-64c65193"),
        data={
            "from": "A Fair Share <notification@afairshare.com>",
            "to": email_list,
            "subject": "A Fair Share",
            "text": message
        }
    )

def receive():
    amqp_setup.check_setup()
    queue_name = 'Notification'

    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()

def callback(channel, method, properties, body):
    data = json.loads(body)
    fullname = data['contact_details']['fullname']
    email_list = data['contact_details']['email_list']

    email_type = data['email_type']

    message_details = data['message_details']

    if email_type == 'place_order':
        payment_amount = message_details['payment_amount']
        order_id = message_details['order_id']
        item_list = message_details['item_list']

        message = f'''
        Dear {fullname},\n\n
        Your order {order_id}, has been placed successfully.\n
        Payment of ${payment_amount} has been received for the following items:{ItemListDisplay(item_list)}\n\n
        Thank you for supporting A Fair Share! :)
        '''
    elif email_type == 'fulfill_order':
        item_name = message_details['item_name']

        message = f'''
        Dear Valued Customer,\n\n
        The item {item_name} has reached it's required order quota and is on it's way to you!\n\n
        - A Fair Share
        '''
    elif email_type == 'archive_order':
        item_name = message_details['item_name']

        message = f'''
        Dear Valued Customer,\n\n
        Thank you for patronising A Fair Share.\n
        Unfortunately, the item {item_name} has not reached it's required order quota and has thus been cancelled. 
        A refund will be processed and you can expect the refund amount to reach you in a few days.\n
        You can have a look at all our other listings at https://a-fair-share-beta.vercel.app/\n\n
        - A Fair Share
        '''

    send_simple_message(email_list, message)

def ItemListDisplay(item_list):
    output = ''

    for item in item_list:
        name = item["item_name"]
        quantity = item["quantity"]
        output += f'\n{name} x{quantity}\n'
    
    output += '\n'

    return output


if __name__ == "__main__":
    receive()
