import pandas as pd
import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


def read():
    # dataframes = {}
    users = os.listdir('data')
    train = []
    test = []
    index = 0
    for user in users:
        files = os.listdir('data/' + user)
        for file in files:
            file_name = "data/" + user + "/" + file  # File name
            if "u-turnings" in file.lower() and index < 4:
                if len(train) == 0:
                    train.append(pd.read_excel(file_name))
                else:
                    train[0] = pd.concat([train[0], pd.read_excel(file_name)], axis=0)
            else:
                test.append(pd.read_excel(file_name))
            index += 1
    print(train)
    print(test)
    return train[0], test[0]
    # print(dataframes)
    # tf.convert_to_tensor(dataframes['user-01-0'])

def read_files():
    train = pd.read_excel('data/user-02-0/STISIMData_U-Turnings.xlsx')
    file2 = pd.read_excel('data/user-03-0/STISIMData_U-Turnings.xlsx')
    #file3 = pd.read_excel('data/user-04-0/STISIMData_U-Turnings.xlsx')
    file4 = pd.read_excel('data/user-05-0/STISIMData_U-Turnings.xlsx')
    test = pd.read_excel('data/user-06-0/STISIMData_U-Turnings.xlsx')
    #train = pd.concat([file1, file2], axis=0)
    #train = pd.concat([train, file3], axis=0)
    #train = pd.concat([train, file4], axis=0)
    return train, test

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
               ]
    return df.drop(columns=columns)


def check_min_max(df, column: str):
    return df.drop(df[(df[column] < 0) | (df[column] > 65535)].index)


def normalize(x, y):
    if x - y > 0:
        return 1
    if x - y == 0:
        return 0
    if x - y < 0:
        return -1


def normalize_clutch(x):
    return 1 if x > 0 else 0


def normalize_gear(x, y):
    if x - y > 0:
        return 1
    if x - y < 0:
        return -1


def normalize_maneuver_marker_flag(x):
    return 1 if x % 2 == 0 else 0


def read_tfds(df):
    # df = pd.read_excel(file)
    df = delete_columns(df)
    df = check_min_max(df, 'Gas pedal')
    df = check_min_max(df, 'Brake pedal')
    df = check_min_max(df, 'Clutch pedal')

    for i in df.index:
        df['speed'][i] = normalize(df['speed'][i], df['speed'][i - 1]) if i != 0 \
            else normalize(df['speed'][i], 0)

        df['RPM'][i] = normalize(df['RPM'][i], df['RPM'][i - 1]) if i != 0 \
            else normalize(df['RPM'][i], 0)

        df['Steering wheel angle'][i] = normalize(df['Steering wheel angle'][i], df['Steering wheel angle'][i - 1]) \
            if i != 0 else normalize(df['Steering wheel angle'][i], 0)

        df['Gas pedal'][i] = normalize(df['Gas pedal'][i], df['Gas pedal'][i - 1]) if i != 0 \
            else normalize(df['Gas pedal'][i], 0)

        df['Brake pedal'][i] = normalize(df['Brake pedal'][i], df['Brake pedal'][i - 1]) if i != 0 \
            else normalize(df['Brake pedal'][i], 0)

        df['Clutch pedal'][i] = normalize_clutch(df['Clutch pedal'][i])

        df['Gear'][i] = normalize(df['Gear'][i], df['Gear'][i - 1]) if i != 0 \
            else normalize(df['Gear'][i], 0)

        df['Maneuver marker flag'][i] = normalize_maneuver_marker_flag(df['Maneuver marker flag'][i])

    x = df.drop('Maneuver marker flag', axis=1)
    y = pd.get_dummies(df['Maneuver marker flag'])

    return x, y


if __name__ == '__main__':
    train, test = read_files()

    xtrain, ytrain = read_tfds(train)
    xtest, ytest = read_tfds(test)
