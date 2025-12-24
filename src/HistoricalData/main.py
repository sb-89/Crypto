from datetime import datetime

from src.Binance.request import getBTCSymbols, getHistoricalKLine
from src.util.file import writeKlinesToCSV


def main():
    btcSymbols = getBTCSymbols()
    print(btcSymbols)
    startDate = datetime(2024, 1, 1)
    endDate = datetime(2024, 8, 1)

    for symbol in btcSymbols:
        writeKlinesToCSV(symbol, getHistoricalKLine(symbol, startDate, endDate))


if __name__ == "__main__":
    main()