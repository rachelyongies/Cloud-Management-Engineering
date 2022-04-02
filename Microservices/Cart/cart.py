#unedited 
import string
import random

from datetime import datetime
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Cart(db.Model):
    __tablename__ = 'cart'
    user_id = db.Column(db.String(15), primary_key=True, nullable=False)
    item_id = db.Column(db.String(15), primary_key=True)
    user_qty = db.Column(db.Integer, nullable=False)
    


    def __init__(self, item_id, category, item_name, item_qty, item_desc, item_price, status):
        self.user_id = user_id
        self.item_id = item_id
        self.user_qty = user_qty
        self.item_price = item_price


    def json(self):
        return {
            "user_id": self.user_id,
            "item_id": self.item_id,
            "user_qty": self.user_qty,
            "item_price": self.item_price,
        }


class Image(db.Model):
    __tablename__ = 'item_image'
    item_id = db.Column(db.String(15), primary_key=True)
    image_url = db.Column(db.String(700), primary_key=True)

    def __init__(self,  item_id, image_url):
        self.item_id = item_id
        self.image_url = image_url

    def json(self):
        return {
            "item_id": self.item_id,
            "image_url": self.image_url
        }


db.create_all()

# add to cart
@app.route("/cart/all", methods=['POST'])
def addToCart():

    data = request.get_json() #get item added
    user_id = data["user_id"] #get user id
    item_list = data['items'] #get item with id and qty

    for item in item_list:
        item_id = item['item_id'] 
        qty = item['quantity']

    cart = Cart(user_id, item_id, qty, datetime.now())
    
    try:
        db.session.add(cart)
        db.session.commit()
        
    except:
        name = 'Add to Cart Error'
        message = f"Error when adding to cart, for item with item_id={item_id}."

        return jsonify(
             {
                "code": 500,
                "data": {
                    "item_id":item_id
                },
                "message": "An error occurred while adding this item to cart."
                    
            }
        ),500


# get ALL items 
@app.route("/cart/all")
def get_all():
    cartlist = Cart.query.all()
    output = []
    for item in cartlist:  # item is an object
        item_image = Image.query.filter_by(
            item_id=item.item_id).first()  # object row

        if item_image is None:
            img_url = None
        else:
            img_url = item_image.image_url

        item_dict = item.json()
        item_dict['image_url'] = img_url
        output.append(item_dict)

    if len(output):
        return jsonify(
            {
                "code": 200,
                "message": "OK",
                "items": output

            }
        ), 200
    return jsonify(
        {
            "code": 500,
            "message": "No items added."
        }
    ), 500
    #3end




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
