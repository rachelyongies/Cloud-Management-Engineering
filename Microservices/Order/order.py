from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
# from amqp_invoke import order_invoke

import string 
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':299}

db = SQLAlchemy(app)

CORS(app)  

class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.String(15), primary_key=True)
    user_id = db.Column(db.String(15), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    #relationship with other tables
    order = db.relationship(
        'Order_Item', backref='order')

    def __init__(self, order_id, user_id, created):
        self.order_id = order_id
        self.user_id = user_id
        self.created = created

    def json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "created": self.created
        }
    
    


class Order_Item(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.String(15), primary_key=True)
    order_id = db.Column(db.String(15), db.ForeignKey('order.order_id'),primary_key=True,nullable=False)

    #book_id = db.Column(db.String(13), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    
    
    def __init__(self, order_id, item_id, quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity

    def json(self):
        return {'order_id': self.order_id, 'item_id': self.item_id, 'quantity': self.quantity}

db.create_all()

@app.route("/order/<string:user_id>")
def get_all_user_orders(user_id):
    
    orderlist = Order.query.filter_by(user_id = user_id).all()
        
    if len(orderlist): 
        return jsonify(
            {
                "code": 200,
                "data": [order.json() for order in orderlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message":  "There are no orders."
        }
    ), 404


@app.route("/order", methods=['POST'])
def create_order():
    #when user posts an order, that order will be posted on both order and order_item database
    
    order_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
    
    data = request.get_json() #get data
    user_id = data["user_id"] #gets user_id
    item_list = data['items'] #gets items with item id and qty
    
        
    order = Order(order_id, user_id, datetime.now()) #puts the body data into the table class Order 

    try:
   
        db.session.add(order)
       
        db.session.commit()
        
    except:
        name = 'Create Order Error'
        message = f"Error when creating an order, for order with order_id={order_id}."
        

        return jsonify(
             {
                "code": 500,
                "data": {
                    "order_id":order_id
                },
                "message": "An error occurred while creating the order."
                    
            }
        ),500
        
    for item in item_list:
        order_item = Order_Item(order_id, item['item_id'], item['quantity'])
        try:
            db.session.add(order_item)
            db.session.commit()

        except:
            # name = 'order_item creation error'
            # message = f"Error when creating the order_item, for order with order_id={order_id}."
            # order_invoke('Error', name, message)

            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "order_id":order_id
                    },
                    "message": "An error occurred while creating the order_item."
                        
                }
            ),500

    # name = 'Order and Order Item creation'
    # message = f"Successfully created Order and Order Item, for order with order_id={order_id}."
    # order_invoke('Log', name, message)        
    return jsonify(
        {
            "code": 201,
            "message": "Order and Order Item has been created",
            "order_id": order_id
        }
    ),201         


@app.route("/order/users/<string:item_id>")
def get_users_for_item(item_id):

    order_rows = Order_Item.query.filter_by(item_id = item_id).all()
    order_list = []
    for row in order_rows:
        if row.order_id not in order_list:
            order_list.append(row.order_id)

    if len(order_list) == 0:
        return jsonify({
            "code": 404,
            "message": "There are no current orders for that item_id."
        }), 404

    user_rows = Order.query.filter(Order.order_id.in_(order_list)).all()
    user_list = []
    for row in user_rows:
        if row.user_id not in user_list:
            user_list.append(row.user_id)

    if len(user_list):
        return jsonify({
            "code": 200,
            "user_list": user_list
        }), 200

    return jsonify({
            "code": 500,
            "message": "Unable to retrieve user_list."
        }), 500


if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5300, debug = True)
