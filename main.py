import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans


def read():
    users = os.listdir('data')
    dataframes = []
    for user in users:
        files = os.listdir('data/' + user)
        for file in files:
            file_name = "data/" + user + "/" + file  # File name
            if "u-turnings" in file.lower():
                dataframes.append(pd.read_excel(file_name))

    return pd.concat(dataframes)


def read_files():
    train = pd.read_excel('data/user-02-0/STISIMData_U-Turnings.xlsx')
    file2 = pd.read_excel('data/user-03-0/STISIMData_U-Turnings.xlsx')
    # file3 = pd.read_excel('data/user-04-0/STISIMData_U-Turnings.xlsx')
    file4 = pd.read_excel('data/user-05-0/STISIMData_U-Turnings.xlsx')
    test = pd.read_excel('data/user-06-0/STISIMData_U-Turnings.xlsx')
    # train = pd.concat([file1, file2], axis=0)
    # train = pd.concat([train, file3], axis=0)
    # train = pd.concat([train, file4], axis=0)
    return train, test


def delete_columns(df):
    columns = ['Accidents',
               'Collisions',
               'Peds Hit',
               'Speeding Tics',
               'Red Lgt Tics',
               'Speed Exceed',
               'Stop Sign Ticks',
               'Throttle input',
               'Brake pedal force',
               'Hand wheel torque',
               'Elapsed time'
               ]
    return df.drop(columns=columns)


def check_min_max(df, column: str):
    return df.drop(df[(df[column] < 0) | (df[column] > 65535)].index)


def normalize(x, y):
    #print(x, y)
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
    return "NO" if x % 2 == 0 else "YES"


def read_tfds(df, t):
    df = delete_columns(df)
    df = check_min_max(df, 'Gas pedal')
    df = check_min_max(df, 'Brake pedal')
    df = check_min_max(df, 'Clutch pedal')


    for index, rows in df.iterrows():
        # for i in df.index:
        df.loc[index, 'speed'] = normalize(rows['speed'], df.iloc[index - 1]['speed']) if index != 0 \
            else normalize(rows['speed'], 0)

        df.loc[index, 'RPM'] = normalize(rows['RPM'], df.iloc[index - 1]['RPM']) if index != 0 \
            else normalize(rows['RPM'], 0)

        df.loc[index, 'Steering wheel angle'] = normalize(rows['Steering wheel angle'], df.iloc[index - 1]['Steering wheel angle']) \
            if index != 0 else normalize(rows['Steering wheel angle'], 0)

        df.loc[index, 'Gas pedal'] = normalize(rows['Gas pedal'], df.iloc[index - 1]['Gas pedal']) if index != 0 \
            else normalize(rows['Gas pedal'], 0)

        df.loc[index, 'Brake pedal'] = normalize(rows['Brake pedal'], df.iloc[index - 1]['Brake pedal']) if index != 0 \
            else normalize(rows['Brake pedal'], 0)

        df.loc[index, 'Clutch pedal'] = normalize_clutch(rows['Clutch pedal'])

        df.loc[index, 'Gear'] = normalize(rows['Gear'], df.iloc[index - 1]['Gear']) if index != 0 \
            else normalize(rows['Gear'], 0)

        df.loc[index, 'Long Dist'] = normalize(rows['Long Dist'], df.iloc[index - 1]['Long Dist']) if index != 0 \
            else normalize(rows['Long Dist'], 0)

        df.loc[index, 'Lat Pos'] = normalize(rows['Lat Pos'], df.iloc[index - 1]['Lat Pos']) if index != 0 \
            else normalize(rows['Lat Pos'], 0)

        df.loc[index, "Maneuver marker flag"] = normalize_maneuver_marker_flag(rows['Maneuver marker flag'])

    x = df.drop('Maneuver marker flag', axis=1)
    y = pd.get_dummies(df['Maneuver marker flag'])

    return df


if __name__ == '__main__':
    data = read()
    data1 = data.dropna(subset=['speed', 'RPM', 'Steering wheel angle', 'Gas pedal', 'Brake pedal', 'Clutch pedal',
                                'Gear', 'Maneuver marker flag', 'Long Dist', 'Lat Pos'])
    #dfr = data1.rolling(window=5).mean()
    df = read_tfds(data1, 0)
    df.to_csv("result.csv", index=False)

    """train, test = read_files()

    xtrain, ytrain = read_tfds(train, 1)
    xtest, ytest = read_tfds(test, 1)"""

    """X = np.array(xtrain)
    y = np.array(ytrain)
    X2 = np.array(xtest)
    y2 = np.array(ytest)

    X.shape

    kmeans = KMeans(n_clusters=2).fit(X)
    centroids = kmeans.cluster_centers_
    print(centroids)"""
