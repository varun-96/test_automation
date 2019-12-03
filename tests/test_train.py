import os

def test_data_path(path='DATA/Iris.csv'):
    assert os.path.exists(path)