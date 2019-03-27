from .ParsedData import ParsedData
from datetime import timedelta
from datetime import datetime


def data_manipulation(parsed_data):
    """
    :type parsed_data: list of ParsedData
    """
    start_date = parsed_data[0].parsedTime
    end_date = parsed_data[len(parsed_data)-1].parsedTime
    index = 0
    while start_date < end_date:
        index += 1
        start_date += timedelta(minutes=60)
        if not time_exists(parsed_data, start_date):
            missed_data = ParsedData()
            missed_data.tOutside = average(parsed_data, index, "tOutside")
            missed_data.tInside = average(parsed_data, index, "tInside")
            missed_data.tSetPoint = average(parsed_data, index, "tSetPoint")
            missed_data.energy = average(parsed_data, index, "energy")
            missed_data.time = start_date.strftime("%Y-%m-%d %H:%M:%S")
            missed_data.parsedTime = datetime.strptime(missed_data.time, "%Y-%m-%d %H:%M:%S")
            parsed_data.insert(index, missed_data)

    return parsed_data


def time_exists(parsed_data, time):
    """
        :param time: datetime
        :type parsed_data: list of ParsedData
    """
    exist = False
    for item in parsed_data:
        if item.parsedTime == time:
            exist = True

    return exist


def average(parsed_data, index, name):
    if index > 2:
        return (getattr(parsed_data[index - 1], name) + getattr(parsed_data[index - 2], name)) / 2
    else:
        return getattr(parsed_data[index - 1], name)


def group_by_day(parsed_data):
    """
       :type parsed_data: list of ParsedData
    """
    start_date = parsed_data[0].parsedTime
    end_date = parsed_data[len(parsed_data)-1].parsedTime
    result = []
    while start_date < end_date:
        new_data = ParsedData()
        new_data.tOutside = average_per_day(parsed_data, start_date.strftime("%Y-%m-%d"), "tOutside")
        new_data.tInside = average_per_day(parsed_data, start_date.strftime("%Y-%m-%d"), "tInside")
        new_data.tSetPoint = average_per_day(parsed_data, start_date.strftime("%Y-%m-%d"), "tSetPoint")
        new_data.energy = average_per_day(parsed_data, start_date.strftime("%Y-%m-%d"), "energy")
        new_data.time = start_date.strftime("%Y-%m-%d")
        new_data.parsedTime = datetime.strptime(new_data.time, "%Y-%m-%d")
        result.append(new_data)

        start_date += timedelta(days=1)

    return result


def average_per_day(parsed_data, day, name):
    data_sum = 0
    count = 0
    for idx, item in enumerate(parsed_data):
        if item.parsedTime.strftime("%Y-%m-%d") == day:
            data_sum += getattr(parsed_data[idx], name)
            count += 1
    return data_sum / count
