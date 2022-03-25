import amqp_setup
import pika
import json

from datetime import datetime

def order_invoke(record_type, name, message):
  body = {
    "record_type": record_type,
    "log_type": "order",
    "name": name,
    "description": message,
    "datetime": datetime.now().isoformat()
  }

  amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='activity.log', 
    body=json.dumps(body), properties=pika.BasicProperties(delivery_mode = 2))

def item_invoke(record_type, name, message):
  body = {
    "record_type": record_type,
    "log_type": "item",
    "name": name,
    "description": message,
    "datetime": datetime.now().isoformat()
  }

  amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='activity.log', 
    body=json.dumps(body), properties=pika.BasicProperties(delivery_mode = 2))

def user_invoke(record_type, name, message):
  body = {
    "record_type": record_type,
    "log_type": "user",
    "name": name,
    "description": message,
    "datetime": datetime.now().isoformat()
  }

  amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='activity.log', 
    body=json.dumps(body), properties=pika.BasicProperties(delivery_mode = 2))

def notification_invoke(email_type, email_list, message_details, fullname=None):
  body = {
    "email_type": email_type,
    "contact_details": {
      "fullname": fullname,
      "email_list": email_list,
    },
    "message_details": message_details
  }

  amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='notification', 
    body=json.dumps(body), properties=pika.BasicProperties(delivery_mode = 2))