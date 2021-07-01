import numpy as np
from sklearn.linear_model import LinearRegression

def find_slope_intercept(independent, dependent):
    assert(len(dependent) == len(independent))

    independent = np.array(independent).reshape((-1, 1))
    dependet = np.array(dependent)

    model = LinearRegression()
    model = model.fit(independent, dependent)
    
    return model.intercept_, model.coef_