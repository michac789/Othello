""" 
Learning File
"""

import sklearn
import sys

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python trainer.py <data>")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = sklearn.load_data(sys.argv[1])
    x_train, x_test, y_train, y_test = sklearn.train_test_split(
        evidence, labels, test_size = 0.2
    )

    # Train model and make predictions
    model = train_model(x_train, y_train)
    predictions = model.predict(x_test)
    

def load_data(dir):
    raise NotImplementedError


def train_model(x_train, y_train):
    raise NotImplementedError
    # regressor = sklearn.LinearRegression()
    # regressor.fit(x_train, y_train)
    # pass


def retrieve_coef():
    raise NotImplementedError


if __name__ == "__main__":
    main()
