"""
This is a sample trainer file, used to test both linear regression and logistic regression supervised learning technique using sample files.
Sample1.csv is trained using linear regression, while sample2.csv is trained using logistic regression.
Assuming you are in the main 'Othello' directory, launch the file immediately to train sample1.csv and sample2.csv.
Some analytics from both linear and logistic regression will be printed out on the terminal window.
Please note that this is only using some arbitrary data, and not used to train the othello heuristic function.
"""

import sklearn
import sklearn.model_selection
import sklearn.metrics
import csv
import os
from sklearn import linear_model


# Load training data, split into training and test sets, train and analyze model
def main():
    # (1) Linear Regression:
    parameters, real_values = load_data(os.path.join("learning_data", "sample1.csv"), 1)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        parameters, real_values, test_size = 0.2
    )
    model = train_model_linreg(x_train, y_train)
    predictions = model.predict(x_test)
    analyze_model_linreg(model, y_test, predictions)
    
    # (2) Logistic Regression


# Load the necessary data from the csv file, divide into a list of all parameters value and another vector list of all expected values
def load_data(dir, type):
    with open(dir) as file:
        next(file)
        reader = csv.reader(file)
        parameters, real_values = [], []
        for row in reader:
            parameters.append([int(row[0]), int(row[1]), int(row[2])])
            if type == 1: real_values.append(int(row[3]))
            elif type == 2: real_values.append(row[2])
    return (parameters, real_values)


# Using linear regression to train a model
def train_model_linreg(x_train, y_train):
    regressor = linear_model.LinearRegression()
    regressor.fit(x_train, y_train)
    return regressor


# Using logistic regression to train a model
def train_model_logreg(x_train, y_train):
    raise NotImplementedError


# Print out the coefficients gained and mean squared error from the test data (linear regression)
def analyze_model_linreg(model, y_test, predictions):
    print("Coefficients gained: \n", model.coef_)
    print("Mean squared error: %.2f" % sklearn.metrics.mean_squared_error(y_test, predictions))


# ??? (logistic regression)
def analyze_model_logreg(model, y_test, predictions):
    raise NotImplementedError


if __name__ == "__main__":
    main()
