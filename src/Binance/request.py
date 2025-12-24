import math
from datetime import datetime, timezone, timedelta

import requests

from src.util.enums import MAX_DAY_DELTA


def ping():
    x = requests.get("https://data-api.binance.vision/api/v3/ping")

    if x.status_code == 200:
        return True
    else:
        return False


'''
    Get ExchangeInfo
'''
def getExchangeInfo():
    exchangeInfoResponse = requests.get("https://data-api.binance.vision/api/v3/exchangeInfo")
    return exchangeInfoResponse.json()

def getBTCSymbols():
    json = getExchangeInfo()
    btcPairs = []
    for obj in json["symbols"]:
        if "BTC" in obj["symbol"]:
            btcPairs.append(obj["symbol"])

    return btcPairs

'''
    Get historical Kline for a single symbol
'''
def getHistoricalKLine(symbol, startDate, endDate, timeinterval="1h"):
    epochStart = math.trunc(startDate.replace(tzinfo=timezone.utc).timestamp()) * 1000
    epochEnd = math.trunc(endDate.replace(tzinfo=timezone.utc).timestamp()) * 1000

    list = []
    # cap of 200 days date in a single request
    if (delta := (endDate - startDate).days) > MAX_DAY_DELTA:
        iterations = math.ceil(delta / MAX_DAY_DELTA)
        for n in range(iterations):
            if delta > MAX_DAY_DELTA:
                days = MAX_DAY_DELTA
            else:
                days = delta

            endDate = startDate + timedelta(days=days)
            epochEnd = math.trunc(endDate.replace(tzinfo=timezone.utc).timestamp()) * 1000

            request = requests.get(
                "https://data-api.binance.vision/api/v3/klines?symbol={}&startTime={}&endTime={}&interval={}".format(
                    symbol, epochStart, epochEnd, timeinterval))

            list += request.json()

            startDate = endDate
            epochStart = math.trunc(startDate.replace(tzinfo=timezone.utc).timestamp()) * 1000

            delta -= days

    else:
        request = requests.get(
            "https://data-api.binance.vision/api/v3/klines?symbol={}&startTime={}&endTime={}&interval={}".format(
                symbol, epochStart, epochEnd, timeinterval))

        list.append(request.json)

    return list

'''
    Get historical Klines for a list of symbols e.g ETHBTC
'''
def getHistoricalKlinesSymbols(symbols, startDate, endDate, timeinterval="1h"):
    epochStart = math.trunc(startDate.replace(tzinfo=timezone.utc).timestamp()) * 1000
    epochEnd = math.trunc(endDate.replace(tzinfo=timezone.utc).timestamp()) * 1000
    list = []
    for str in symbols:
        request = requests.get(
            "https://data-api.binance.vision/api/v3/klines?symbol={}&startTime={}&endTime={}&interval={}".format(
                str, epochStart, epochEnd, timeinterval))
        list.append(request.json())
    return list


def main():
    online = ping()
    print("true" if online else "false")
    # btcPairs = getBTCPairs()
    startDate = datetime(2024, 1, 1)
    endDate = datetime(2024, 8, 1)
    delta = endDate - startDate
    print(delta.days)
    getHistoricalKLine("ETHBTC", startDate, endDate)
    # getHistoricalKlinesPairs(btcPairs, startDate, endDate)

if __name__ == "__main__":
    main()