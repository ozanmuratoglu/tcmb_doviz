from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

def get_exchange_rates():
    url = 'https://www.tcmb.gov.tr/kurlar/today.xml'
    response = requests.get(url)
    tree = ET.fromstring(response.content)

    rates = {'TRY': 1.0}
    for currency in tree.findall('Currency'):
        code = currency.get('CurrencyCode')
        rate_text = currency.find('ForexSelling').text
        if rate_text:
            rate = float(rate_text.replace(',', '.'))
            rates[code] = rate
    return rates

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    rates = get_exchange_rates()
    currencies = sorted(rates.keys())

    amount = ''
    from_curr = 'TRY'
    to_curr = 'USD'

    if request.method == 'POST':
        from_curr = request.form['from_currency']
        to_curr = request.form['to_currency']
        amount = request.form['amount']

        if from_curr in rates and to_curr in rates and amount:
            try:
                amount_float = float(amount)
                result = amount_float * rates[to_curr] / rates[from_curr]
            except ValueError:
                result = "Geçersiz miktar girdiniz."

    return render_template(
        'index.html',
        currencies=currencies,
        result=result,
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr
    )

if __name__ == '__main__':
    app.run(debug=True)
