import pandas as pd
from definitions import trade_model_X_columns
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score as auc

data = pd.read_csv('C:/Users/Edan Berrett/Desktop/sample_data.csv')
data['player_won_play_from_state_game'] = data[
                        'previous_player_won_play_from_state_game'].shift(-1)

trade_model_rows = data[data['trade_player_relative_position'].notna()]

trade_model_X = trade_model_rows[trade_model_X_columns]
trade_model_Y = trade_model_rows['player_won_play_from_state_game']

(   
 
    trade_model_X_train,
    trade_model_X_test,
    trade_model_Y_train,
    trade_model_Y_test
    
) = train_test_split(trade_model_X,trade_model_Y)

trade_model = XGBClassifier(
        min_child_weight=100
    ).fit(trade_model_X_train,trade_model_Y_train)

predictions = [p[1] for p in trade_model.predict_proba(trade_model_X_train)]

print(auc(trade_model_Y_train,predictions))

predictions = [p[1] for p in trade_model.predict_proba(trade_model_X_test)]

print(auc(trade_model_Y_test,predictions))