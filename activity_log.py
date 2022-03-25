import json
import amqp_setup

from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':299}
 
db = SQLAlchemy(app)

CORS(app)

class Log(db.Model):
    __tablename__ = 'log'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_type = db.Column(db.String(10), nullable=False)
    log_type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, record_type, log_type, name, datetime, description):
        self.record_type = record_type
        self.log_type = log_type
        self.name = name 
        self.datetime = datetime 
        self.description = description 

    def json(self):
        return {
            "record_type": self.record_type,
            "log_type": self.log_type,
            "name": self.name,
            "datetime": self.datetime,
            "description": self.description
        }

db.create_all()

def receive():
    amqp_setup.check_setup()
    queue_name = 'Activity_Log'

    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()

def callback(channel, method, properties, body):
    data = json.loads(body)
    data["datetime"] = datetime.fromisoformat(data["datetime"])

    log = Log(**data)
 
    try:
        db.session.add(log)
        db.session.commit()

    except Exception as e:
        print(e)

if __name__ == '__main__':
    receive()
