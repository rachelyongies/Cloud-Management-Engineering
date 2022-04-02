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


class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.String(15), primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(50), nullable=False)
    item_qty = db.Column(db.Integer, nullable=False)
    item_desc = db.Column(db.String(150), nullable=False)
    item_price = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(15), nullable=False)

    def __init__(self, item_id, category, item_name, item_qty, item_desc, item_price, status):
        self.item_id = item_id
        self.category = category
        self.item_name = item_name
        self.item_qty = item_qty
        self.item_desc = item_desc
        self.item_price = item_price
        self.status = status

    def json(self):
        return {
            "item_id": self.item_id,
            "category": self.category,
            "item_name": self.item_name,
            "item_qty": self.item_qty,
            "item_desc": self.item_desc,
            "item_price": self.item_price,
            "status": self.status,
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


# get ALL items 
@app.route("/item/all")
def get_all():
    itemlist = Item.query.all()
    output = []
    for item in itemlist:  # item is an object
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
            "message": "No items exist."
        }
    ), 500
    #3end



# get all items with selected status (w 1 image URL)
@app.route("/item/all/<string:status>")
def get_all_with_status(status):
    itemlist = Item.query.filter_by(
        status=status).all()  # gets item with status
    output = []

    for item in itemlist:  # item is an object
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
            "code": 404,
            "message": "Item does not exist."
        }
    ), 404

# get specific item with item_id (w all the image URLs)
@app.route("/item/<string:item_id>")
def get_item(item_id):

    # get one item details from Item
    # object
    itemDetails = Item.query.filter_by(item_id=item_id).first()

    # get all item images from Image
    item_images = Image.query.filter_by(item_id=item_id).all()

    itemDetails = itemDetails.json()

    img_list = []
    # for each image in images
    for img in item_images:
        img_list.append(img.image_url)

    itemDetails['images'] = img_list

    if len(itemDetails):
        return jsonify(
            {
                "code": 200,
                "message": "OK",
                "item_details": itemDetails

            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Item does not exist."
        }
    ), 404

# set pending status
@app.route("/item/setpendingstatus/<string:item_id>", methods=['PUT'])
def setpendingstatus(item_id):
    row = Item.query.filter_by(item_id=item_id).first()
    if (row.status == 'pending'):
        row.status = 'shipping'
        try:
            db.session.commit()
        except:
            name = 'Item Status Change'
            message = f"Error when changing item status from 'Pending' to 'Shipping', for item with item_id={item_id}."

            return jsonify(
                {
                    "code": 500,
                    "message": 'Error occurred while changing status.'
                }
            ), 500

    name = 'Item Status Change'
    message = f"The item status for item with item_id={item_id}, has just been changed from 'Pending' to 'Shipping'."

    return jsonify(
        {
            "code": 200,
            "message": 'OK.',
            "item_name": row.item_name
        }
    ), 200

# set shipping status
@app.route("/item/setshippingstatus/<string:item_id>", methods=['PUT'])
def setshippingstatus(item_id):
    row = Item.query.filter_by(item_id=item_id).first()
    if (row.status == 'shipping'):
        row.status = 'complete'
        try:
            db.session.commit()
        except:
            name = 'Item Status Change'
            message = f"Error when changing item status from 'Shipping' to 'Complete', for item with item_id={item_id}."

            return jsonify(
                {
                    "code": 500,
                    "message": 'Error occurred while changing status.'
                }
            ), 500

    name = 'Item Status Change'
    message = f"The item status for item with item_id={item_id}, has just been changed from 'Shipping' to 'Complete'."

    return jsonify(
        {
            "code": 200,
            "message": 'OK.'
        }
    ), 200

# set archive status when item is pending
@app.route("/item/setarchivestatus/<string:item_id>", methods=['PUT'])
def setarchivestatus(item_id):
    row = Item.query.filter_by(item_id=item_id).first()

    if row is None:
        return jsonify(
            {
                "code": 400,
                "message": "Item not found."
            }
        )

    if (row.status == 'pending'):
        row.status = 'archived'
        try:
            db.session.commit()
        except:
            name = 'Item Status Change'
            message = f"Error when changing item status from 'Pending' to 'Archived', for item with item_id={item_id}."

            return jsonify(
                {
                    "code": 500,
                    "message": 'Error occurred while changing status.'
                }
            ), 500

        name = 'Item Status Change'
        message = f"The item status for item with item_id={item_id}, has just been changed from 'Pending' to 'Archived'."

        return jsonify(
            {
                "code": 200,
                "message": 'OK.',
                "item_name": row.item_name
            }
        ), 200
    else:
        name = 'Item Status Change'
        message = f"Error when archiving item as status is not pending, for item with item_id={item_id}."

        return jsonify(
            {
                "code": 400,
                "message": "Unable to archive item as item status is not pending."
            }
        ), 400


# find item by category
@app.route("/item/category/<string:category>")
def find_by_category(category):
    itemList = Item.query.filter_by(category=category).all()
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "message": 'OK.',
                "data": [item.json() for item in itemList]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message":  "Item category does not exist."
        }
    ), 404


# add to 2 tables image and item
@app.route("/item", methods=['POST'])
def add_item():
    data = request.get_json()
    item_id = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(15)])

    category = data["category"]
    item_name = data["item_name"]
    item_qty = data["item_qty"]
    item_desc = data["item_desc"]
    item_price = data["item_price"]
    status = 'pending'
    image_url = data["image_url"]

    item = Item(item_id, category, item_name, item_qty, item_desc,
                item_price, status)
    item_json = item.json()

    try:
        db.session.add(item)
        db.session.commit()

    except:
        name = 'Item Creation'
        message = f"Error when adding item, for item with item_id={item_id}."

        return jsonify(
            {
                "code": 500,
                "message": 'Error occurred while adding item.'
            }
        ), 500

    for url in image_url:
        item_image = Image(item_id, url)
        try:
            db.session.add(item_image)
            db.session.commit()

        except:
            name = 'Item Creation'
            message = f"Error when adding item_image, for item with item_id={item_id}."

            return jsonify(
                {
                    "code": 500,
                    "message": 'Error occurred while adding item_image.'
                }
            ), 500


    name = 'Item Creation'
    message = f"The item with item_id={item_id}, has been successfully added into the db."

    return jsonify(
        {
            "code": 201,
            "message": 'Item successfully created.'
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
