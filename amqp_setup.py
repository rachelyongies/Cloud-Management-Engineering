import pika
from os import environ

# These module-level variables are initialized whenever a new instance of python interpreter imports the module;
# In each instance of python interpreter (i.e., a program run), the same module is only imported once (guaranteed by the interpreter).

hostname = 'host.docker.internal'
port = environ.get("rabbit_port")

# connect to the broker and set up a communication channel in the connection
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=hostname, port=port,
            heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
    ))
except Exception as e:
    print(e)

channel = connection.channel()

exchangename="central_exchange"
exchangetype="topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

############   Activity_Log queue    #############
queue_name = 'Activity_Log'
channel.queue_declare(queue=queue_name, durable=True)

channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='activity.log') 

############   Notification queue    #############
queue_name = 'Notification'
channel.queue_declare(queue=queue_name, durable=True)

channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='notification') 

def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype)


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
