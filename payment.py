import stripe

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

stripe.api_key = "sk_test_51IZYDIC3YOFFC7Y0ESAsy21lEn22fTU5vXI0rIfwGQMpoRRvkLKGhcmqyEADmEhqox2beLhC006HRzb0UAoKEwJd00GUHNVlk1"

@app.route('/payment', methods=['POST'])
def pay():
  data = request.get_json()
  data['amount'] = int(float(data['amount']) * 100)

  # Create a card token
  try:
    card_token = stripe.Token.create(
      card={
        "number": data['card_number'],
        "exp_month": data['expiry_month'],
        "exp_year": data['expiry_year'],
        "cvc": data['cvv'],
        "name": data['cardholder_name'],
      },
    )
  except stripe.error.CardError as e:
    return jsonify({
      "http_status" : e.http_status,
      "code" : e.code,
      "param" : e.param,
      "user_message" : e.user_message,
    }), 400
  except Exception as e:
    return jsonify({
      "code": 400,
      "message": "Card creation unsuccessful",
      "error": e
    }), 400

  # Charge the card
  try:
    response = stripe.Charge.create(
      amount=data['amount'],
      currency="sgd",
      source=card_token,
      description="description here",
    )
  except stripe.error.CardError as e:
    print(e)
    return jsonify({
      "http_status" : e.http_status,
      "code" : e.code,
      "param" : e.param,
      "user_message" : e.user_message,
    }), 400
  except Exception as e:
    return jsonify({
      "code": 400,
      "message": "Charge unsuccessful",
      "error": e
    }), 400

  return response, 200


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5004, debug=True)
