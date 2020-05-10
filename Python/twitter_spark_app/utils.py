from datetime import datetime, timedelta
import json, csv, os.path
from os import remove
from shutil import move

def country_list():
    return json.load(open('woeid/countries.json', 'r'))


def city_list(city):
    data = json.load(open('woeid/cities_by_country.json', 'r'))
    possible_countries = set()
    for country in data:
        if city in data.get(country):
            possible_countries.add(country)
    return possible_countries


""" Marked as private even though it is not in a class - more like a hint that it's used in another util func"""
def _line_exists_in_file(file_path, line_in):
    data_file = open(file_path, 'r')
    lines = [line.strip('\n') for line in data_file.readlines()]
    data_file.close()
    i = 0
    while i < len(lines):
        if line_in == lines[i]:
            return True
        else:
            i += 1
    return False


def last_n_days_from(date, delta):
    date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d') - timedelta(delta), '%Y-%m-%d')
    return date


""" Marked as private even though it is not in a class - more like a hint that it's used in another util func"""
def _cleanup_file(src_name):
    dir = 'output/'
    tmp_name = src_name.split('.')[-2] + '_tmp.' + src_name.split('.')[-1]

    with open(dir+"/"+src_name, 'r', encoding='utf-8') as inFile, \
         open(dir+"/"+tmp_name, 'w', encoding='utf-8') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)

    move(os.path.join(dir, tmp_name),
         os.path.join(dir, src_name))


def list_of_n_dates_from(date, delta):
    return [last_n_days_from(date, i) for i in range(0, delta)]


def write_to_csv(file_name, topic, date, count):
    file_path_orig = file_name
    file_path = 'output/{}'.format(file_name)
    with open(file_path, mode='a', newline='') as oFile:
        headers = ["term", "date", "count"]
        line = "{topic},{date},{count}".format(topic=topic, date=date, count=count)
        writer = csv.DictWriter(oFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)

        # TODO: add header if file exists but is empty, right now it doesn't add it, only if file is non-existent
        if oFile.tell() == 0:
            print(">> Creating a new file [{}].. and adding header".format(file_path))
            writer.writeheader()
            writer.writerow(
                {"term": topic,
                 "date": date,
                 "count": count})
            oFile.write("\n")
        else:
            if not _line_exists_in_file(file_path, line):
                print(">> Appending data to file [%s]" % file_path)
                writer.writerow(
                    {"term": topic,
                     "date": date,
                     "count": count})
                oFile.write("\n")
            else:
                print(">> Skip writing data to file [%s]. It already exists" % file_path)

    _cleanup_file(file_path_orig)


def get_date_n_days_ago(delta):
    date = datetime.strftime(datetime.now() - timedelta(delta), '%Y-%m-%d')
    return date

