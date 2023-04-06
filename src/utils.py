import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

'''
    This function helps to write and save the pickle object (preprocessor or model) toa .pickle file
'''
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

'''
    A function to perform following in each model: 
        1. tune hyperparameters to find best parameters
        2. train the model with best parameters
        3. save trained model 
        4. evaluate the model and calcualte r2 score for each
'''
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}
        num_models = len(list(models))
        print(f'We are training {num_models} models')
        
        for model_key, model_obj in models.items():
            hyper_params = param[model_key]

            print(f'Training {model_key} model with parameters: {hyper_params}')
            
            # perform the hyper parameter tuninig using grid search
            gs = GridSearchCV(model_obj,hyper_params,cv=3)
            gs.fit(X_train,y_train)
            
            # set the best parameters to the model and train the model
            model_obj.set_params(**gs.best_params_)
            model_obj.fit(X_train,y_train)

            # perform predictions for train and test data and calculate r2 scores 
            y_train_pred = model_obj.predict(X_train)
            y_test_pred = model_obj.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            print(f'r2 value for {model_key}: {test_model_score}')
            
            # save the r2 score in the report
            report[model_key] = test_model_score
            
        return report

    except Exception as e:
        raise CustomException(e, sys)


'''
    This function helps to load the pickle object file (preprocessor or model) when we have to use them
'''
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
