"""
This is a sample trainer file, used to test both linear regression and logistic regression supervised learning technique using sample files.
Sample1.csv is trained using linear regression, while sample2.csv is trained using logistic regression.
Assuming you are in the main 'Othello' directory, launch the file immediately to train sample1.csv and sample2.csv.
Some analytics from both linear and logistic regression will be printed out on the terminal window.
Please note that this is only using some arbitrary data, and not the one used to train the othello heuristic function.
"""

import sklearn
import sklearn.model_selection
import sklearn.linear_model
import sklearn.metrics
import csv
import os
import pickle


# Load training data, split into training and test sets, train and analyze model, getting result from new data
def main():
    # (1) Linear Regression:
    x_train1, x_test1, y_train1, y_test1 = load_data(os.path.join("sample.csv"), 1)
    linreg_model = train_model_linreg(x_train1, y_train1)
    predictions1 = linreg_model.predict(x_test1)
    analyze_model_linreg(linreg_model, y_test1, predictions1)
    
    # (2) Logistic Regression
    x_train2, x_test2, y_train2, y_test2 = load_data(os.path.join("learning_data", "sample2.csv"), 2)
    logreg_model = train_model_logreg(x_train2, y_train2)
    predictions2 = logreg_model.predict(x_test2)
    analyze_model_logreg(logreg_model, y_test2, predictions2)
    
    # Save model in a wav file
    print("Saving models...")
    save_path_1 = os.path.join("learning_data", "sample_linreg.sav")
    save_path_2 = os.path.join("learning_data", "sample_logreg.sav")
    pickle.dump(linreg_model, open(save_path_1, 'wb'))
    pickle.dump(logreg_model, open(save_path_2, 'wb'))
    print("Models saved.\n")

    # Using the saved models to predict result based on some evidences
    # Expected func: y=3a1+2a2-a3; 10, 7, 6, 4; win win lose lose
    loaded_model1 = pickle.load(open(save_path_1, 'rb'))
    loaded_model2 = pickle.load(open(save_path_2, 'rb'))
    data = [[6, 1, 10], [4, 2, 9], [1, 2, 1], [1, 2, 3]]
    make_predictions(data, loaded_model1, loaded_model2)


# Load the necessary data from the csv file, divide into training and test parameters and outcome, return those values
def load_data(dir, type):
    with open(dir) as file:
        next(file)
        reader = csv.reader(file)
        parameters, real_values = [], []
        for row in reader:
            parameters.append([int(row[0]), int(row[1]), int(row[2])])
            # if type == 1: real_values.append(int(row[3]))
            # elif type == 2: real_values.append(row[3])
    print(parameters)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(parameters, real_values, test_size = 0.2)
    return (x_train, x_test, y_train, y_test)


# Using linear regression to train a model
def train_model_linreg(x_train, y_train):
    regressor = sklearn.linear_model.LinearRegression()
    regressor.fit(x_train, y_train)
    return regressor


# Using logistic regression to train a model
def train_model_logreg(x_train, y_train):
    logreg = sklearn.linear_model.LogisticRegression()
    logreg.fit(x_train, y_train)
    return logreg


# Print out the coefficients gained and mean squared error from the test data (linear regression)
def analyze_model_linreg(model, y_test, predictions):
    print("Linear Regression")
    print("Coefficients gained: \n", model.coef_)
    print("Mean squared error: %.2f\n" % sklearn.metrics.mean_squared_error(y_test, predictions))


# Print out the true positive (win) rate and true negative (lose) rate (logistic regression)
def analyze_model_logreg(model, y_test, predictions):
    print("Coefficients gained: \n", model.coef_)
    positive_labels_count, negative_labels_count, positive_labels_accurate, negative_labels_accurate = 0, 0, 0, 0
    for label, prediction in zip(y_test, predictions):
        if label == "win":
            positive_labels_count += 1
            if label == prediction: positive_labels_accurate += 1
        elif label == "lose":
            negative_labels_count += 1
            if label == prediction: negative_labels_accurate += 1
    print("Logistic Regression")
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    if positive_labels_count != 0:
        sensitivity = positive_labels_accurate / positive_labels_count # True positive rate (percentage when 'win' is guessed correctly)
        print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    else: print("True Positive Rate: Undetermined (not enough test data)")
    if negative_labels_count != 0:
        specificity = negative_labels_accurate / negative_labels_count # True negative rate (percentage when 'lose' is guessed correctly)
        print(f"True Negative Rate: {100 * specificity:.2f}%")
    else: print("True Negative Rate: Undetermined (not enough test data)")
    print("")


# Based on model 1 (linear regression) and model 2 (logistic regression), print the predicted outcome based on the test cases
def make_predictions(test_cases, model1, model2):
    print("Predictions based on test cases:")
    print(model1.predict(test_cases))
    print(model2.predict(test_cases))
    print(model2.predict_proba(test_cases))
    print("")


if __name__ == "__main__":
    main()
