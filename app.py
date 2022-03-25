from flask import Flask
from schema import Query
from flask_graphql import GraphQLView
from graphene import Schema
import os

app = Flask(__name__)

view_func = GraphQLView.as_view(
    'graphql', schema=Schema(query=Query), graphiql=True)

app.add_url_rule('/graphql', view_func=view_func)

@app.route('/')
def hello_world():
    return "A-Fair-Share GraphQL"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)