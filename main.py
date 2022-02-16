import pandas as pd
import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


def read():
    dataframes = {}
    users = os.listdir('data')
    for user in users:
        files = os.listdir('data/' + user)
        for file in files:
            file_name = "data/" + user + "/" + file  # File name
            if "u-turnings" in file.lower():
                dataframes[user] = pd.read_excel(file_name)
    # print(dataframes)
    tf.convert_to_tensor(dataframes['user-01-0'])


def delete_columns(df):
    columns = ['Accidents',
               'Collisions',
               'Peds Hit',
               'Speeding Tics',
               'Red Lgt Tics',
               'Speed Exceed',
               'Stop Sign Ticks',
               'Elapsed time',
               'Long Dist',
               'Lat Pos',
               'Throttle input',
               'Brake pedal force',
               'Hand wheel torque',
               'Maneuver marker flag'
               ]
    return df.drop(columns=columns)


def check_min_max(df, column: str):
    return df.drop(df[(df[column] < 0) | (df[column] > 65535)].index)


def normalize_speed(x):
    print(x)
    if x > 1:
        return 1
    if x == 0:
        return 0
    if x < 0:
        return -1


def read_tfds():
    path = 'data/user-02-0/STISIMData_U-Turnings.xlsx'
    df = pd.read_excel(path)
    df = delete_columns(df)
    print(df.columns)
    df = check_min_max(df, 'Gas pedal')
    df = check_min_max(df, 'Brake pedal')
    df = check_min_max(df, 'Clutch pedal')

    #df['Gas pedal'] = df['speed'].apply(normalize_speed)
    # df['Brake pedal'] = df['speed'].apply(normalize_speed)
    # df['Clutch pedal'] = df['speed'].apply(normalize_speed)
    # print(df['speed'])
    # df.drop()


if __name__ == '__main__':
    # read()
    read_tfds()
