import logging
import os

import requests

logger = logging.getLogger(__name__)

host = os.environ.get('COIN_HOST')

def query_price_by_ids(ids: str, vs_currencies: str) -> dict:
    """
    Query the price of a cryptocurrency by its ID.

    Args:
        ids (str): coins' ids, comma-separated if querying more than 1 coin. Defaults to "bitcoin".
        vs_currencies (str): target currency of coins, comma-separated if querying more than 1 currency. Defaults to "usd".

    Returns:
        dict: price(s) of cryptocurrency.
    """
    logger.info(f'Querying price of {ids} in {vs_currencies}')

    # return {'bitcoin': {'usd': 94282}}

    url = host + '/api/v3/simple/price'
    params = {
        'ids': ids,
        'vs_currencies': vs_currencies
    }
    headers = {
        'accept': 'application/json',
        'x-cg-pro-api-key': os.environ.get('COIN_API_KEY')
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Failed to query price: {response.status_code}')
        return {}

def query_historical_data_by_ids(ids: str,
                                 vs_currency: str,
                                 days: int) -> dict:
    """
    This endpoint allows you to get the historical chart data of a coin including time in UNIX, price, market cap and 24hrs volume based on particular coin id.

    Args:
        ids (str): coins' ids, comma-separated if querying more than 1 coin. Defaults to "bitcoin".
        vs_currency (str): target currency of market data. Defaults to "usd".
        days (int): number of days to retrieve data for. Defaults to 7.
    Returns:
        dict: historical data of cryptocurrency.
    """
    logger.info(f'Querying historical data of {ids} in {vs_currency}')
    url = host + '/api/v3/coins/id/market_chart'
    params = {
        'ids': ids,
        'vs_currency': vs_currency,
        'days': days
    }
    headers = {
        'accept': 'application/json',
        'x-cg-pro-api-key': os.environ.get('COIN_API_KEY')
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Failed to query historical data: {response.status_code}')
        return {}

def query_markets_by_ids(vs_currency: str) -> dict:
    """
    This endpoint allows you to query all the supported coins with price, market cap, volume and market related data.

    Args:
        vs_currency (str): target currency of coins, comma-separated if querying more than 1 currency. Defaults to "usd".

    Returns:
        dict: markets where cryptocurrency is traded.
    """
    logger.info(f'Querying markets data of {vs_currency}')
    url = host + '/api/v3/coins/id/tickers'
    params = {
        'vs_currency': vs_currency,
        # 'ids': ids
    }
    headers = {
        'accept': 'application/json',
        'x-cg-pro-api-key': os.environ.get('COIN_API_KEY')
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Failed to query markets data: {response.status_code}')
        return {}

def send_http_request(method: str, url: str, headers: dict, params: dict) -> dict:
    try:
        headers = headers or {}
        headers['x-cg-pro-api-key'] = os.environ.get('COIN_API_KEY')

        response = requests.request(method, url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error(f'Failed to query markets data: {response.status_code}')
            return {"error": "request error"}
    except Exception as e:
        logger.error(f"Error sending HTTP request: {e}")
    return {}

if __name__ == '__main__':
    print(query_price_by_ids("bitcoin", "usd"))