import requests
import json
from collections import namedtuple
from graphene import ObjectType, String, Int, DateTime, Field, List, Schema, Float, Mutation, InputObjectType, Boolean, Mutation
import os

item_URL = os.environ.get('item_URL')
order_URL = os.environ.get('order_URL')
user_URL = os.environ.get('user_URL')

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

class Item(ObjectType):
    item_id = String()
    category = String()
    item_name = String()
    item_qty = Int()
    item_desc = String()
    item_price = Float()
    current_count = Int()
    shipping_count = Int()
    status = String()
    expiry = String()
    image_url = String()

class User(ObjectType):
    user_type = String()
    user_id = String()
    user_password = String()
    fullname = String()
    email = String()
    phone_number = String()

class Address(ObjectType):
    user_id = String()
    postal_code = Int()
    city = String()
    address = String()
    country = String()

class creditCard(ObjectType):
    user_id = String()
    card_number = String()
    cardholder_name = String()
    cvv = Int()
    expiry_month = String()
    expiry_year = String()

class Order(ObjectType):
    order_id = String()
    user_id = String()
    created = DateTime()

class OrderItem(ObjectType):
    item_id = String()
    order_id = String()
    qty = Int()

class activityLog(ObjectType):
    user_id = String()
    record_id = String()
    log_type = String()
    name = String()
    datetime = String()
    description = String()

class Query(ObjectType):
    items = List(Item)
    items_by_status = List(Item, status=String(required=True))
    item_by_id = List(Item, item_id=String(required=True))
    items_by_cat = List(Item, category=String(required=True))
    user_by_id = List(User, user_id=String(required=True), address=String(required=True))
    user_address = List(Address, user_id=String(required=True))
    credit_card = List(creditCard, user_id=String(required=True))
    user_order = List(Order, user_id=String(required=True))
    activity_log = List(activityLog, record_id=String(required=True))

    def resolve_items(root, info):
        endpoint = item_URL + "all"
        print(endpoint)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['items'])
            all_items = json2obj(data)
            return all_items

    def resolve_items_by_status(root, info, **kwargs):
        # Get all items
        status = kwargs.get('status')
        endpoint = item_URL + "all/" + status
        response = requests.get(endpoint) 
        if response.status_code == 200:
            data = json.dumps(response.json()['items'])
            all_items = json2obj(data)
            return all_items

    def resolve_item_by_id(root, info, **kwargs):
        item_id = kwargs.get('item_id')
        endpoint = item_URL + item_id
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['items'])
            all_items = json2obj(data)
            all_items = [all_items]
            return all_items

    def resolve_items_by_cat(root, info, **kwargs):
        category = kwargs.get('category')
        endpoint = item_URL + "category/" + category
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['data'])
            cat_items = json2obj(data)
            return cat_items

    def resolve_user_by_id(root, info, **kwargs):
        user_id = kwargs.get('user_id')

        endpoint = user_URL + "details/" + user_id
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['details'])
            user = json2obj(data)
            user = [user]
            return user

    def resolve_user_address(root, info, **kwargs):
        user_id = kwargs.get('user_id')

        endpoint = user_URL + user_id + "/addresses"
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['data']['addresses'])
            address = json2obj(data)
            return address
    
    def resolve_credit_card(root, info, **kwargs):
        user_id = kwargs.get('user_id')

        endpoint = user_URL + user_id + "/credit_cards"
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['data']['credit_cards'])
            credit_card = json2obj(data)
            return credit_card

    def resolve_user_order(root, info, **kwargs):
        user_id = kwargs.get('user_id')

        endpoint = order_URL + user_id
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = json.dumps(response.json()['data']['order'])
            order = json2obj(data)
            return order
    
    