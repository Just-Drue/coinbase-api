from collections import OrderedDict

import requests
from flask import Flask, render_template, request

try:
    from config import http_proxy, https_proxy

    proxies = {
        'http': http_proxy,
        'https': https_proxy
    }
except (ImportError, http_proxy, https_proxy):
    proxies = {}

app = Flask(__name__)

coins = {
    'Bitcoin': 'BTC-EUR',
    'Ethereum': 'ETH-EUR'
}


@app.route('/', methods=['GET', 'POST'])
def index(response=None):
    post_data = {'amount': None, 'coin': None}

    if request.method == 'POST':
        post_data = {k: v for k, v in (val.split('=') for val in (request.get_data().decode('utf8').replace("'", '"').split('&')))}
        response = requests.get(
            url=f'https://api.pro.coinbase.com/products/{coins[post_data["coin"]]}/ticker',
            headers={'Content-Type': 'application/json'},
            proxies=proxies
        ).json()

        if post_data['amount'] == '':
            post_data['amount'] = 0

        response = (OrderedDict({
            'price': '{:,}'.format(float(response['price'])),
            'bid': '{:,}'.format(float(response['bid'])),
            'last_price': '{:,}'.format(round(float(response['price']) * float(post_data['amount']), 2)),
            'last_bid': '{:,}'.format(round(float(response['bid']) * float(post_data['amount']), 2))
        }))
    return render_template('index.html', coins=coins.keys(), amount=response,
                           input_value=post_data['amount'], coin_type=post_data['coin'])


if __name__ == '__main__':
    app.run(debug=True)
