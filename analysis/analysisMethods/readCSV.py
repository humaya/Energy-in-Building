import csv
from .ParsedData import ParsedData
from datetime import datetime


def read_csv(file):
    with open(file) as data:
        csv_data = csv.reader(data, delimiter=';')
        data_result = []
        for row in csv_data:
            item = ParsedData()
            item.time = row[0]
            item.parsedTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            item.energy = float(row[1])
            item.tOutside = float(row[2])
            item.tInside = float(row[3])
            item.tSetPoint = float(row[4])
            data_result.append(item)

    return data_result

