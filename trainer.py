"""
Learning File
"""

import sklearn
import sklearn.model_selection
import sklearn.metrics
import sys
import csv
from sklearn import linear_model


def main():
    # Ensure correct usage, load training data, split into training and test sets
    if len(sys.argv) != 2:
        sys.exit("Usage: python trainer.py <data>")
    parameters, real_values = load_data(sys.argv[1])
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        parameters, real_values, test_size = 0.01
    )

    # Train model, then displaying some analytical data based on the learning
    model = train_model(x_train, y_train)
    analyze_model(model)


# Load the necessary data from the csv file, divide into a list of all parameters value and another vector list of all expected values
def load_data(dir):
    with open(dir) as file:
        next(file)
        reader = csv.reader(file)
        parameters, real_values = [], []
        for row in reader:
            parameters.append([int(row[0]), int(row[1])])
            real_values.append(int(row[2]))
    return (parameters, real_values)


# Using linear regression to train the model, given a list of parameters (x) and expected value (y) from the training data
def train_model(x_train, y_train):
    regressor = linear_model.LinearRegression()
    regressor.fit(x_train, y_train)
    return regressor


# Print out the coefficients, make further analysis of the data... #TODO
def analyze_model(model):
    print("Coefficients: \n", model.coef_)


if __name__ == "__main__":
    main()
