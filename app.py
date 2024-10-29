
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(data)

    # Access the first element from 'unit-currency' and 'currency-name' lists
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]

    # Fetch conversion factor and calculate final amount
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    
    # Prepare response
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"
    headers = {
        "X-RapidAPI-Key": "9b11a98d50mshb8fcfd476f9032ap101988jsn87d4a403a2b2",  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "exchangerate-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract the conversion factor for the target currency
    cf = float(data['rates'].get(target, 1))  # Default to 1 if the currency is not found
    return cf

if __name__ == "__main__":
    app.run(debug=True)
