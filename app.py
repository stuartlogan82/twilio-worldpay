from dotenv import load_dotenv
from flask import Flask, session, request
from os import environ
from twilio.twiml.voice_response import Gather, VoiceResponse, Say, Redirect
import json
import requests


load_dotenv()


SECRET_KEY = environ.get('SECRET_KEY')
app = Flask(__name__)
app.secret_key = SECRET_KEY

###
# If you want your interaction to start here, you can uncomment the below route.
# More commonly you would gather information about the caller and the amount to pay in
# another flow and pass the attributes in  as query params to the make_payment route
###

# @app.route('/welcome', methods=['GET', 'POST'])
# def welcome():
#     caller = request.form.get('Caller')
#     call_sid = request.form.get('CallSid')
#     session['caller'] = caller
#     session['call_sid'] = call_sid
#     response = VoiceResponse()
#     if caller == "+447412345678":
#         session['caller_name'] = 'Stuart'
#         response.say("Thanks for calling, Stuart")
#     else:
#         response.say("Thanks for calling")

#     response.redirect('/make_payment')
#     return str(response)


def get_or_append_details(option, prompt):
    digits = request.form.get('Digits')
    response = VoiceResponse()
    if digits:
        session[option] = digits
        response.redirect('/make_payment')
    else:
        gather = Gather(timeout=3)
        gather.say(
            prompt)
        response.append(gather)

    return str(response)


@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    response = VoiceResponse()
    if 'caller_name' not in session:
        session['caller_name'] = request.args.get(
            'caller_name') or "Twilio Payment"
    if 'payment_amount' not in session:
        session['payment_amount'] = request.args.get('amount') or "5000"
    if 'card_number' not in session:
        response.redirect('/get_card_number')
    elif 'expiry' not in session:
        response.redirect('/get_expiry')
    elif 'cvv' not in session:
        response.redirect('/get_cvv')
    else:
        call_sid = request.form.get('CallSid')
        session['call_sid'] = call_sid
        response.redirect('/process_payment')

    return str(response)


@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    url = 'https://api.worldpay.com/v1/orders'
    headers = {'Authorization': environ.get('WORLDPAY_API_KEY'),
               'Content-type': 'application/json'}
    body = {
        "paymentMethod": {
            "type": "Card",
            "name": session['caller_name'],
            "expiryMonth": session['expiry'][:2],
            "expiryYear": f"20{session['expiry'][2:]}",
            "cardNumber": session['card_number'],
            "cvc": session['cvv'],
            "issueNumber": "1"
        },
        "orderType": "ECOM",
        "orderDescription": session['call_sid'],
        "amount": session['payment_amount'],
        "currencyCode": "GBP"}
    r = requests.post(url, headers=headers, data=json.dumps(body))
    requests.post(environ.get('END_OF_INTERACTION_URL'), r.text)
    response = VoiceResponse()
    response.say("Payment processed, goodbye")
    # If your flow started in Twilio Studio, redirect back to it to complete the call
    # response.redirect(
    #     'https://webhooks.twilio.com/v1/Accounts/ACfd0573f9f976b99746c693XXXXXXXXXX/Flows/FWbfdeda0a21644267231d3dXXXXXXXXXX?FlowEvent=return')
    return str(response)


@app.route('/get_card_number', methods=['GET', 'POST'])
def get_card_number():
    return get_or_append_details('card_number', "Please enter your credit card number")


@app.route('/get_expiry', methods=['GET', 'POST'])
def get_expiry():
    return get_or_append_details('expiry', "Please enter your expiry date, two digits for the month and two digits for the year")


@app.route('/get_cvv', methods=['GET', 'POST'])
def get_cvv():
    return get_or_append_details('cvv', 'Please enter your CVV. Typically this is the 3 digit number on the back of your card')
