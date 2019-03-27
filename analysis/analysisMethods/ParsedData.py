from django.core import serializers


class ParsedData:
    time = ""
    """
    :type parsedTime: datetime
    """
    parsedTime = ""
    energy = 0
    tOutside = 0
    tInside = 0
    tSetPoint = 0

    svr_rbf = 0
    svr_lin = 0
    svr_poly = 0

    lr = 0
