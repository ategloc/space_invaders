import json


def write_to_json(file_handle, score):
    data = [{'highscore': score}]
    json.dump(data, file_handle)


def read_from_json(file_handle):
    data = json.load(file_handle)
    return data
