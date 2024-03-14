from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
stripe.api_key = "sk_test_51OqjevGueFI8a5iZU7p2CPvQcQ89PjXNPZ4UHzJN559DrDaZlSnsfraCymuRdNskAyUnCXRWSzTPT22yZIdsMLFl00RYM2MJcv"


@app.route('/api/payment', methods=['POST'])
def create_stripe_user():
    """
    Creates a new Stripe user with the given payment method and email.

    Parameters:
        p_method (str): The payment method to associate with the new user.
        email (str): The email address of the new user.

    Returns:
        tuple: A tuple containing a string indicating the success status ('success' if successful, None otherwise) and the created customer object if successful, or a tuple containing None and the error message if unsuccessful.
    """
    data = request.get_json()
    p_method = data['payment_method_id']
    amount = data['amount']
    try:
        customer = stripe.Customer.create(
            payment_method=p_method
        )

        if customer:
            if create_stripe_intent(customer, p_method, amount):
                return jsonify({'message': 'Payment successful'}), 200
        return jsonify({'message': 'Payment failed'}), 400
    except Exception as e:
        return jsonify({'message': 'Payment failed'}), 400


def create_stripe_intent(customer, payment_method, amount):
    """
    Create a Stripe payment intent.

    Args:
        customer (str): The ID of the customer to associate the payment with.
        payment_method (str): The ID of the payment method to use.
        amount (float): The amount to charge, in USD.

    Returns:
        tuple: A tuple containing a string representing the status of the payment ('success' or None) and a PaymentIntent object.

    Raises:
        Exception: If there is an error creating the payment intent.

    Example:
        create_stripe_intent('customer_id', 'payment_method_id', 10.0)
    """
    try:
        intent = stripe.PaymentIntent.create(
            customer=customer,
            payment_method=payment_method,
            currency='usd',  # you can provide any currency you want
            amount=int(float(amount) * 100),  # I modified the amount to distinguish payments
            off_session=True,
            confirm=True
        )

        return intent
    except Exception as e:
        return None, str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
