import utils


def test_list_of_n_dates_from():
    date = ['2020-05-14', '2020-05-13']
    assert date == utils.list_of_n_dates_from('2020-05-14', 2)

