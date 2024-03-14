from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
stripe.api_key = "sk_test_51OqjevGueFI8a5iZU7p2CPvQcQ89PjXNPZ4UHzJN559DrDaZlSnsfraCymuRdNskAyUnCXRWSzTPT22yZIdsMLFl00RYM2MJcv"


@app.route('/payment-intent', methods=['POST'])
def payment_sheet():
    data = request.get_json()
    if data['authKey'] != "abc":
        return jsonify({'error': 'Invalid authKey'})
    # Use an existing Customer ID if this is a returning customer
    customer = stripe.Customer.create()
    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
    )
    paymentIntent = stripe.PaymentIntent.create(
        amount=1099,
        currency='eur',
        customer=customer['id'],
        # In the latest version of the API, specifying the `automatic_payment_methods` parameter
        # is optional because Stripe enables its functionality by default.
        automatic_payment_methods={
            'enabled': True,
        },
    )
    return jsonify(paymentIntent=paymentIntent.client_secret,
                   ephemeralKey=ephemeralKey.secret,
                   customer=customer.id,
                   publishableKey='pk_test_51OqjevGueFI8a5iZePhWA5uF1VRm8M4EepWfUc3GEC26vXvXkVB9pbdC4XBldLLZJjbb2mtZLHAqiI3ZXRuPfbWx00Ayl9gulj'

                   )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
