import pickle
import pandas as pd
import datetime as dt

def predict_bikes():
    address = "Custom House" # callback
    st = './stations/'+address+'.pkl'
    day = dt.datetime.today().weekday()
    hour = (dt.datetime.now().hour) + 3 # current hour + 3
    rain = 1 # can use an sql query to get this

    # SELECT round(threeH_rain_predict * 100) FROM weather;

    with open(st,'rb') as input:
        rfc = pickle.load(input)

    df = pd.DataFrame({'HOUR': [hour],  'rain_in_mm': [rain]})
    df_dummies_DOW = pd.DataFrame({'DOW_Monday': [1], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})

    for i in df_dummies_DOW:
        if day == 0:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [1], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
        elif day == 1:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [1],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
        elif day == 2:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [1], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
        elif day == 3:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [1],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
        elif day == 4:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [1], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
        elif day == 5:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [1],'DOW_Sunday': [0]})
        else:
            df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [1]})

    df_cont_feat = df[['HOUR','rain_in_mm']]
    X = pd.concat([df_cont_feat, df_dummies_DOW[['DOW_Monday', 'DOW_Tuesday','DOW_Wednesday', 'DOW_Thursday','DOW_Friday', 'DOW_Saturday','DOW_Sunday']]], axis =1)

    print(rfc.predict(X))

if __name__ == "__main__":
    predict_bikes()
    
