import gc
from pyexpat import model
from joblib import dump, load
import pandas as pd
import os
import icecream as ic
import pprint
import matplotlib.pyplot as plt
import numpy as np


# import xgboost as xgb
from lightgbm import LGBMClassifier

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_validate, KFold  # k-fold Cross Validation
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
from sklearn import metrics


# DATA_FILEPATH = os.path.join('app', 'data', 'cs-training.csv')
# MODEL_FILEPATH = os.path.join('app', 'models', 'model.joblib')
# path_1 = "/Users/mathieugrosso/Desktop/Workspace_Git/AI_Advanced/my_model_api/model"


MODEL_PATH = "/Users/mathieugrosso/Desktop/X-HEC-entrepreneurs/IA-advanced/my_model_api/Kaggle_Competitions/tabular_playground_series/model/"
DATA_FILEPATH = os.path.join('data', '')


scores = {'A': [], 'B': []}
test_predictions = {'A': [], 'B': []}


def run_model(test, key):
    test_predictions = []
    for dirname, _, filenames in os.walk('../model'):
        for i in filenames:
            if key in i:
                model_path = os.path.join(MODEL_PATH, i)
                print(model_path)
                model = load(model_path)
                test_predictions.append(model.predict_proba(test)[:, 1])
                print(np.mean(test_predictions))
    return np.mean(test_predictions)


def run_prediction(input_df, model_A_path, model_B_path):
    for key in test_predictions:
        print(f"Team: {key} ")
        prediction = run_model(input_df, key)

        test_predictions[key].append(prediction)
    return test_predictions


def return_predictions(input_df, model_A_path, model_B_path):
    test_predictions = run_prediction(input_df, model_A_path, model_B_path)

    test_predictions['B'] = test_predictions['B'][0]
    test_predictions['A'] = test_predictions['A'][0]
    print(len(test_predictions['A']))
    test_predictions['team_A_scoring_within_10sec'] = test_predictions['A']
    test_predictions['team_B_scoring_within_10sec'] = test_predictions['B']

    test_predictions['id'] = [i for i in range(
        len(test_predictions['team_A_scoring_within_10sec']))]

    del test_predictions['A']
    del test_predictions['B']
    submission = pd.DataFrame.from_dict(test_predictions)
    submission = submission.to_dict(orient='records')

    return submission


if __name__ == '__main__':
    test_data = """[
{
"id":6, 

  "ball_pos_x": -71.17880249023438,
  "ball_pos_y": 85.4159927368164,
  "ball_pos_z": 22.628000259399414,
  "ball_vel_x": 12.423199653625488,
  "ball_vel_y": 8.449799537658691,
  "ball_vel_z": 4.570400238037109,
  "p0_pos_x": -27.330801010131836,
  "p0_pos_y": 1.0766000747680664,
  "p0_pos_z": 0.3400000035762787,
  "p0_vel_x": -29.969999313354492,
  "p0_vel_y": -5.86359977722168,
  "p0_vel_z": 0.0066000004298985004,
  "p0_boost": 95.6875,
  "p1_pos_x": -79.09020233154297,
  "p1_pos_y": 69.43299865722656,
  "p1_pos_z": 1.8260000944137573,
  "p1_vel_x": 2.0911998748779297,
  "p1_vel_y": 4.958600044250488,
  "p1_vel_z": -8.733599662780762,
  "p1_boost": 31.765625,
  "p2_pos_x": -24.728200912475586,
  "p2_pos_y": 60.234798431396484,
  "p2_pos_z": 0.33980000019073486,
  "p2_vel_x": 22.931398391723633,
  "p2_vel_y": -31.348798751831055,
  "p2_vel_z": 0.004399999976158142,
  "p2_boost": 47.53125,
  "p3_pos_x": -16.364398956298828,
  "p3_pos_y": 35.70159912109375,
  "p3_pos_z": 0.33980000019073486,
  "p3_vel_x": 20.128398895263672,
  "p3_vel_y": 19.75040054321289,
  "p3_vel_z": 0.009200000204145908,
  "p3_boost": 0.0,
  "p4_pos_x": -74.24600219726562,
  "p4_pos_y": 22.412399291992188,
  "p4_pos_z": 0.3208000063896179,
  "p4_vel_x": 7.789999961853027,
  "p4_vel_y": -37.98699951171875,
  "p4_vel_z": 0.18940000236034393,
  "p4_boost": 13.3359375,
  "p5_pos_x": -37.623199462890625,
  "p5_pos_y": 102.06099700927734,
  "p5_pos_z": 9.150199890136719,
  "p5_vel_x": -8.81760025024414,
  "p5_vel_y": -0.04520000144839287,
  "p5_vel_z": 23.152799606323242,
  "p5_boost": 59.59375,
  "boost0_timer": -3.75390625,
  "boost1_timer": 0.0,
  "boost2_timer": -5.8984375,
  "boost3_timer": -5.83203125,
  "boost4_timer": -6.96484375,
  "boost5_timer": -3.787109375
},
 {"id": 7,
  "ball_pos_x": -59.713199615478516,
  "ball_pos_y": -98.21959686279297,
  "ball_pos_z": 16.888399124145508,
  "ball_vel_x": -4.808800220489502,
  "ball_vel_y": 2.544800043106079,
  "ball_vel_z": 11.87279987335205,
  "p0_pos_x": -58.06019973754883,
  "p0_pos_y": -100.78179931640625,
  "p0_pos_z": 12.739398956298828,
  "p0_vel_x": -4.492599964141846,
  "p0_vel_y": 1.8102000951766968,
  "p0_vel_z": 16.53499984741211,
  "p0_boost": 18.046875,
  "p1_pos_x": -29.306201934814453,
  "p1_pos_y": -100.01419830322266,
  "p1_pos_z": 0.5428000092506409,
  "p1_vel_x": -16.111600875854492,
  "p1_vel_y": 5.326400279998779,
  "p1_vel_z": -1.5255999565124512,
  "p1_boost": 100.0,
  "p2_pos_x": -60.29359817504883,
  "p2_pos_y": -87.94339752197266,
  "p2_pos_z": 0.3402000069618225,
  "p2_vel_x": -4.316800117492676,
  "p2_vel_y": 11.55579948425293,
  "p2_vel_z": 0.004999999888241291,
  "p2_boost": 0.7841796875,
  "p3_pos_x": -63.81399917602539,
  "p3_pos_y": -77.606201171875,
  "p3_pos_z": 0.3402000069618225,
  "p3_vel_x": -9.80459976196289,
  "p3_vel_y": 23.415199279785156,
  "p3_vel_z": 0.004000000189989805,
  "p3_boost": 0.0,
  "p4_pos_x": -39.95280075073242,
  "p4_pos_y": 25.078401565551758,
  "p4_pos_z": 0.3402000069618225,
  "p4_vel_x": -30.667400360107422,
  "p4_vel_y": -17.093198776245117,
  "p4_vel_z": -0.0007999999797903001,
  "p4_boost": 9.203125,
  "p5_pos_x": -78.70939636230469,
  "p5_pos_y": -46.398597717285156,
  "p5_pos_z": 0.7573999762535095,
  "p5_vel_x": -23.380800247192383,
  "p5_vel_y": 2.0910000801086426,
  "p5_vel_z": 8.708800315856934,
  "p5_boost": 100.0,
  "boost0_timer": -0.92578125,
  "boost1_timer": 0.0,
  "boost2_timer": 0.0,
  "boost3_timer": -1.0712890625,
  "boost4_timer": 0.0,
  "boost5_timer": -4.34765625},
 {"id": 8,
  "ball_pos_x": 29.671001434326172,
  "ball_pos_y": -96.21080017089844,
  "ball_pos_z": 23.818798065185547,
  "ball_vel_x": 23.862199783325195,
  "ball_vel_y": 3.555799961090088,
  "ball_vel_z": -11.86780071258545,
  "p0_pos_x": -4.78380012512207,
  "p0_pos_y": -82.20280456542969,
  "p0_pos_z": 0.3402000069618225,
  "p0_vel_x": 18.75819969177246,
  "p0_vel_y": -9.178999900817871,
  "p0_vel_z": 0.00419999985024333,
  "p0_boost": 23.921875,
  "p1_pos_x": -12.080999374389648,
  "p1_pos_y": -102.05960083007812,
  "p1_pos_z": 17.996200561523438,
  "p1_vel_x": 5.263800144195557,
  "p1_vel_y": 0.00559999980032444,
  "p1_vel_z": -16.30739974975586,
  "p1_boost": 60.78125,
  "p2_pos_x": 22.185400009155273,
  "p2_pos_y": -101.8666000366211,
  "p2_pos_z": 22.082599639892578,
  "p2_vel_x": 20.851999282836914,
  "p2_vel_y": -0.13740000128746033,
  "p2_vel_z": -9.044000625610352,
  "p2_boost": 47.84375,
  "p3_pos_x": -11.476800918579102,
  "p3_pos_y": -8.652199745178223,
  "p3_pos_z": 0.3402000069618225,
  "p3_vel_x": 18.820600509643555,
  "p3_vel_y": 10.376800537109375,
  "p3_vel_z": 0.00559999980032444,
  "p3_boost": 12.15625,
  "p4_pos_x": 57.861202239990234,
  "p4_pos_y": -58.371402740478516,
  "p4_pos_z": 0.3402000069618225,
  "p4_vel_x": 18.849000930786133,
  "p4_vel_y": -16.406400680541992,
  "p4_vel_z": 0.00039999998989515007,
  "p4_boost": 96.3125,
  "p5_pos_x": 27.241201400756836,
  "p5_pos_y": -101.44960021972656,
  "p5_pos_z": 22.800199508666992,
  "p5_vel_x": 30.81279945373535,
  "p5_vel_y": 2.393399953842163,
  "p5_vel_z": -0.15800000727176666,
  "p5_boost": 0.0,
  "boost0_timer": -5.890625,
  "boost1_timer": 0.0,
  "boost2_timer": -3.19921875,
  "boost3_timer": 0.0,
  "boost4_timer": 0.0,
  "boost5_timer": 0.0}
]"""
    run_model(test_data, 'A')
