from sklearn.svm import SVR
import numpy as np
from .ParsedData import ParsedData


def svr_calculate(parsed_data, support_poly=True, degree_day=True):
    """
       :param degree_day:
       :param support_poly:
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

    if degree_day:
        t_outside_list = np.array(t_outside_list)
        t_set_point_list = np.array(t_set_point_list)
        hd = t_set_point_list - t_outside_list
        HD = list(hd)
        x = [HD]
    else:
        x = [t_outside_list, t_set_point_list]

    X = np.transpose(x)
    y = np.transpose(energy_list)

    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

    y_rbf = svr_rbf.fit(X, y).predict(X)

    for idx, item in enumerate(parsed_data):
        item.svr_rbf = y_rbf[idx]

    if support_poly:
        svr_poly = SVR(kernel='poly', C=1e3, degree=2)
        svr_lin = SVR(kernel='linear', C=1e3)
        y_poly = svr_poly.fit(X, y).predict(X)
        y_lin = svr_lin.fit(X, y).predict(X)
        for idx, item in enumerate(parsed_data):
            item.svr_lin = y_lin[idx]
            item.svr_poly = y_poly[idx]

    return parsed_data
