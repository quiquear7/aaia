import pandas as pd
import os
import numpy as np
import tensorflow as tf


def read():
    users = os.listdir('data')
    for user in users:
        files = os.listdir('data/' + user)
        for file in files:
            file_name = "data/" + user + "/" + file  # File name
            print(file_name)
            df = pd.read_excel(file_name)
            print(df)


if __name__ == '__main__':
    read()
