from ctypes import POINTER, c_double, byref
import numpy as np

NEIGHBORHOOD_SIZE = 10
LOCAL_SIZE_PERCENTAGE = 0.1

COOLING_DECREASE = 0.98
MAX_TEMPERATURE = 1000
MIN_TEMPERATURE = 0.01


def random_neighbor(dimension, bounds, local_area_length, position_original):

    position = []

    for i in range(dimension):

        coordinate = np.random.normal(position_original[i], local_area_length / 2)

        # ensure boundaries
        while not coordinate >= bounds[0] or not coordinate <= bounds[1]:
            coordinate = np.random.normal(position_original[i], local_area_length / 2)
        position.append(coordinate)

    position = np.asarray(position)
    return position


def run(bounds, dimension, cost_function, function_id, max_fes):

    bounds_length = bounds[1] - bounds[0]
    local_area_length = bounds_length * LOCAL_SIZE_PERCENTAGE

    cost_best = np.Inf
    position_best = np.random.uniform(bounds[0], bounds[1], dimension)
    costs_history = []

    fes = 1

    temperature = MAX_TEMPERATURE
    position_original = position_best

    while temperature > MIN_TEMPERATURE and fes <= max_fes:

        # generate points in local area
        for _ in range(NEIGHBORHOOD_SIZE):

            position = random_neighbor(dimension, bounds, local_area_length, position_original)
            c_cost = c_double()
            c_cost_orig = c_double()

            cost_function(position.ctypes.data_as(POINTER(c_double)), byref(c_cost), dimension, 1, function_id)
            cost_function(position_original.ctypes.data_as(POINTER(c_double)), byref(c_cost_orig), dimension, 1, function_id)

            cost = c_cost.value
            cost_orig = c_cost_orig.value
            cost_delta = cost - cost_orig

            fes += 1

            if cost_delta < 0:

                position_original = position

                if cost < cost_best:
                    cost_best = cost
                    position_best = position
            else:
                r = np.random.uniform(0, 1)

                if r < np.exp((-cost_delta) / temperature):
                    position_original = position

            costs_history.append(cost_best)

        temperature *= COOLING_DECREASE

    # fill missing values to target FES
    last_val = costs_history[-1]

    for _ in range(max_fes - len(costs_history)):
        costs_history.append(last_val)

    return costs_history
