from datetime import datetime
import time
import json
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
import argparse

api_key = '92e72e72-94d4-464b-b422-612182b99528'  # Bitcoin API

ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/dCtU1xDDhQLnzMw1hZGldj'  # webhooks URL


def get_latest_bitcoin_price():
    # coin marketcap API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'bitcoin',  # change to get different cryptocurrencies eg. bitcoin,ethereum
        'convert': 'USD'  # calculate market quotes in up to 120 currencies
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()
        # print(json.dumps(data, sort_keys=True, indent=4))
        latest_price = data['data']['1']['quote']['USD']['price']
        return float(latest_price)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = ifttt_webhook_url.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def main(BITCOIN_PRICE_THRESHOLD, interval):
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update',
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 1 minutes
        # (For testing purposes you can set it to a lower number)
        time.sleep(interval * 60)


def cli():

    parser = argparse.ArgumentParser(
        description=' Bitcoin Notifier ')

    # argument for notification

    parser.add_argument(
        '-e',
        default=[10000],
        type=int,
        nargs=1,
        metavar='threshold',
        help=' Enter threshold ',
    )

    # argument for interval

    parser.add_argument(
        '-t',
        metavar='interval',
        default=[5],
        type=int,
        nargs=1,
        help=' Enter time interval',
    )

    parser.add_argument(
        '-d',
        default=['Yes'],
        type=str,
        nargs=1,
        metavar='decision',
        help=' Enter (Yes/No) - Yes will run the program',
    )

    args = parser.parse_args()

    decision = args.d[0]
    if decision == 'Yes':
        main(args.e[0], args.t[0])
    else:
        print('No Notification')


if __name__ == '__main__':
    cli()
