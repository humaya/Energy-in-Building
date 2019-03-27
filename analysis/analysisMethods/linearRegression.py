import numpy as np
from .ParsedData import ParsedData
import pandas as pd
import statsmodels.api as sm


def calculate_lr(parsed_data):
    """
       :type parsed_data: list of ParsedData
    """

    t_outside_list = []
    t_inside_list = []
    t_set_point_list = []
    energy_list = []
    for item in parsed_data:
        t_outside_list.append(item.tOutside)
        t_inside_list.append(item.tInside)
        t_set_point_list.append(item.tSetPoint)
        energy_list.append(item.energy)

    t_outside_list = np.array(t_outside_list)
    t_inside_list = np.array(t_inside_list)
    t_set_point_list = np.array(t_set_point_list)

    hd = t_set_point_list - t_outside_list
    dt = t_set_point_list - t_inside_list

    HD = list(hd)
    DT = list(dt)

    y = pd.DataFrame(energy_list)
    x = [HD, DT]
    xx = pd.DataFrame(x)
    X = np.transpose(xx)

    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)

    for idx, item in enumerate(parsed_data):
        item.lr = predictions[idx]

    return parsed_data
