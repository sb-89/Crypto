from datetime import datetime, timezone
from pathlib import Path
def writeKlinesToCSV(symbol, json):
    if (len(json) != 0):
        path = "../../HistoricalData/Klines/{}".format(symbol)
        Path(path).mkdir(parents=True, exist_ok=True)
        filename = "/{}.csv".format(symbol)
        file = open("../../HistoricalData/Klines/".format(filename), "w")
        date = datetime.fromtimestamp(json[0][0] / 1000, timezone.utc)

        # for entry in date:
        #     if entry[0] > date and entry[0].month > date.month:
        #         date = entry[0]

        file.close()



