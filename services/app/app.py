
from flask import Flask, jsonify, request
from src.predict import return_predictions
import pandas as pd
import os
import numpy as np
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


vel_groups = {
    f"{el}_vel": [f'{el}_vel_x', f'{el}_vel_y', f'{el}_vel_z']
    for el in ['ball'] + [f'p{i}' for i in range(6)]
}

dist_cols = ['p0_pos_dist_ball',
             'p1_pos_dist_ball', 'p2_pos_dist_ball', 'p3_pos_dist_ball',
             'p4_pos_dist_ball', 'p5_pos_dist_ball']

pos_groups = {
    f"{el}_pos": [f'{el}_pos_x', f'{el}_pos_y', f'{el}_pos_z']
    for el in ['ball'] + [f'p{i}' for i in range(6)]
}

model_FILEPATH_A = "/app/models"
model_FILEPATH_B = "/app/models"


@app.route("/")
def hello():
    return "Welcome to machine learning model APIs of Mathieu and Heloise!"


def euclidian_dist(x):
    return np.linalg.norm(x, axis=1)


def add_features(test):
    # absolute speed of the ball:
    array2 = test['ball_vel_x'].values*test['ball_vel_x'].values + test['ball_vel_y'].values * \
        test['ball_vel_y'].values + \
        test['ball_vel_z'].values*test['ball_vel_z'].values
    test["abs_ball_speed"] = [np.sqrt(i) for i in array2]

    # euclidian dist
    for col, vec in pos_groups.items():
        test[col + '_dist_ball'] = euclidian_dist(
            test[vec].values - test[pos_groups["ball_pos"]].values)

    # velocity magnitude
    for col, vec in vel_groups.items():
        test[col] = euclidian_dist(test[vec])

    # closest player to the ball
    test['closest_p_to_ball'] = test[dist_cols].idxmin(axis=1)
    test.replace(['p0_pos_dist_ball',
                  'p1_pos_dist_ball', 'p2_pos_dist_ball', 'p3_pos_dist_ball',
                  'p4_pos_dist_ball', 'p5_pos_dist_ball'], [0, 1, 2, 3, 4, 5], inplace=True)

    return test


@app.route('/predict', methods=['GET'])
def get_predict():
    return 'predict route'


@app.route('/predict', methods=['POST'])
def get_scores():
    # handle datax

    payload = request.json  # get the data

    input_df = pd.DataFrame(payload)

    # process data
    input_df = add_features(input_df)

    input_df = input_df.drop(["id"], axis=1)
    input_df = input_df.drop(["ball_pos_dist_ball", "abs_ball_speed"], axis=1)

    # load all models
    print(input_df)
    predictions = return_predictions(
        input_df, model_FILEPATH_A, model_FILEPATH_B)
    print(predictions)

    # scores = [prediction[1] for prediction in predictions]

    return jsonify(predictions)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
