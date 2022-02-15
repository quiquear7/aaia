import pandas as pd
import os
import numpy as np
import tensorflow as tf


def read():
    dataframes = {}
    users = os.listdir('data')
    for user in users:
        files = os.listdir('data/' + user)
        for file in files:
            file_name = "data/" + user + "/" + file  # File name
            if "u-turnings" in file.lower():
                dataframes[user] = pd.read_excel(file_name)
    print(dataframes)


if __name__ == '__main__':
    read()
