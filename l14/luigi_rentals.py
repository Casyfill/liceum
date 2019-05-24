import json
import pickle
from pathlib import Path

import luigi as lu
import pandas as pd
from sklearn.metrics import (make_scorer, mean_absolute_error,
                             median_absolute_error)
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

this_folder = Path(__file__).parent
# python -m luigi --module luigi_rentals Pull_Data

class Pull_data(lu.Task):
    v = lu.NumericalParameter(default=0.1, var_type=float, 
                              min_value=0, max_value=100)
    
    boro = lu.ChoiceParameter(default='Queens', var_type=str, choices=[
        'Queens', 'Brooklyn', 'Manhattan'
    ])

    prod = lu.BoolParameter()

    def output(self):
        prod_ = "prod" if self.prod else 'staging'
        path = f'data/{prod_}/{self.boro}/raw_{self.v}.csv'
        path = str(this_folder / path)

        return lu.LocalTarget(path)

    # def complete(self):
    #     return self.output().exist()

    # def requires(self):
    #     return ...
    
    def run(self):
        source = f'https://raw.githubusercontent.com/Codecademy/datasets/master/streeteasy/{self.boro.lower()}.csv'
        data = pd.read_csv(source)

        self.output().makedirs()
        data.to_csv(self.output().path)


class Train_Model(lu.Task):
    v = lu.NumericalParameter(default=0.1, var_type=float, 
                              min_value=0, max_value=100)
    
    boro = lu.ChoiceParameter(default='Queens', var_type=str, choices=[
        'Queens', 'Brooklyn', 'Manhattan'
    ])

    prod = lu.BoolParameter()

    def output(self):
        prod_ = "prod" if self.prod else 'staging'
        path = this_folder / f'data/{prod_}/{self.boro}/model_{self.v}'

        return {
            'metrics': lu.LocalTarget(str(path / 'metrics.json')),
            'predicted': lu.LocalTarget(str(path / 'predicted.csv')),
            'model': lu.LocalTarget(str(path / 'model.pkl'))
            }
    
    def requires(self):
        return Pull_data(boro=self.boro, prod=self.prod, v=0.1)
    

    def run(self):
        df = pd.read_csv(self.input().path)
        
        y = df['rent']
        X = df[['bedrooms', 'bathrooms', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs', 'no_fee']]

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8, random_state=2019)
        
        model = XGBRegressor(random_state=2019, max_depth=10, n_estimators=1000)
        model.fit(X_train, y_train)


        pred = model.predict(X_test)
        metrics = {
            'max_depth':10,
            'n_extimators': 1000,
            'test_mae': mean_absolute_error(y_test, pred)
        }

        X_test['predicted'] = pred

        self.output()['predicted'].makedirs()
        X_test.to_csv(self.output()['predicted'].path)
        
        with open(self.output()['metrics'].path, 'w') as f:
            json.dump(metrics, f)

        with open(self.output()['model'].path, 'wb') as f:
            pickle.dump(model, f)
