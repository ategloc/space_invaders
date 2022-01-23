from model_io import write_to_json, read_from_json


def test_write_to_json():
    path = open("highscore.json", "w")
    write_to_json(path, 21377)


def test_read_from_json():
    path = open("highscore.json", 'r')
    my_list = (read_from_json(path))
    print (my_list[0].get('highscore', 0))


# test_read_from_json()
# test_write_to_json()