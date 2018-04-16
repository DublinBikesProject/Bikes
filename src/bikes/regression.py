# Import required packages
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

def prediction(a,b):
    # Read csv file into a dataframe.
    df = pd.read_csv('regression_data.csv')

    X = df[['HOUR','rain_in_mm']]
    y = df.avg_avail_bikes

    dtc = DecisionTreeClassifier(max_depth=3, random_state=1)
    dtc.fit(X, y)

    predictions = dtc.predict(X)
    df_true_vs_predicted = pd.DataFrame({'Actual_bike_numbers': df.avg_avail_bikes, 'Predicted_bike_numbers': predictions})

    scores = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=1), X, y, scoring='mean_absolute_error', cv=3)

    rfc = RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1)
    rfc.fit(X, y)

    rfc_predictions = rfc.predict(X)
    df_true_vs_rfc_predicted = pd.DataFrame({'ActualClass': y, 'PredictedClass': rfc_predictions})

    print("absolute error",metrics.mean_absolute_error(y, rfc_predictions))

    scores = cross_val_score(RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1), X, y, scoring='mean_absolute_error', cv=3)

    print("rf_cv3",abs(scores.mean()))
    

    X_new = pd.DataFrame({'HOUR': [a],  'rain_in_mm': [b]})
    print("prediction",dtc.predict(X_new))

#prediction(18,20)

if __name__ == "__main__":
    prediction(18,20)
