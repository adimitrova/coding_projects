from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.colors
import numpy as np
import random

spark = SparkSession.builder.appName("twitter_stuff").getOrCreate()
# plt.style.use('dark_background')


def _slope(x1, y1, x2, y2):
    """ Coordinates of 2 points on x and y, returns their slope

    :param x1: point A value on X-axis
    :param y1: point A value on Y-axis
    :param x2: point B value on X-axis
    :param y2: point B value on Y-axis
    :return: slope of the 2 points
    """

    # values = list()
    # values.append(slope(2, 5, 1, 10))
    # values.append(slope(1, 10, 3, 15))
    # values.append(slope(3, 15, 4, 10))
    # values.append(slope(4, 10, 5, 20))
    return (y2-y1)/(x2-x1)


def generate_slopes(data):
    print(">> Computing slopes of the data..")
    for item in data:
        i = 0
        while i <= len(data):
            print("Slope of {}, {} & {}, {} = {}".format(item[i][0], item[i][1], item[i+1][0], item[i+1][1],
                                                        int(_slope(x1=item[i][0], y1=item[i][1], x2=item[i+1][0], y2=item[i+1][1]))))
            i += 1
        print("=======")


def generate_x_and_y_values(file_path=None):
    print(">> Fetching data fom file.")
    df = spark.read.csv(file_path, header=True)
    res = df.select("*")
    res.createOrReplaceTempView('output')
    print(">> Fetching distinct dates and terms fom file.")
    distinct_dates = sorted([row['date'] for row in spark.sql("SELECT DISTINCT date FROM output").collect()])
    distinct_terms = [row['term'] for row in spark.sql("SELECT DISTINCT term FROM output").collect()]
    dates_mapping = [(item, i + 1) for i, item in enumerate(distinct_dates)]
    all_settings_list = list()

    for t in distinct_terms:
        y_axis_counts = list()
        x_axis_unmapped_dates = list()
        label = t
        for d in distinct_dates:
            count = [row['count'] for row in spark.sql("SELECT count FROM output WHERE term='{}' AND date='{}'".format(t, d)).collect()][0]
            y_axis_counts.append(int(count))
            x_axis_unmapped_dates.append(str(d))

        # now map dates to numerical values
        x_axis_dates = list()
        for item in x_axis_unmapped_dates:
            for d in dates_mapping:
                if item == d[0]:
                    x_axis_dates.append(d[1])

        paired_data = list(zip(x_axis_dates, y_axis_counts))
        plotting_settings = {
            "term": label,
            "x_axis_dates": x_axis_dates,
            "y_axis_counts": y_axis_counts,
            "output_file": 'plots/{}.png'.format(t),
            "distinct_dates": distinct_dates,
            "paired_data": paired_data,
        }
        all_settings_list.append(plotting_settings)

    return plt, all_settings_list


def plot(plt, **plotting_settings):
    plt.clf()
    colours = ['darkturquoise', 'darkorchid', 'red', 'orangered', 'blue', 'crimson', 'orchid', 'darkviolet', 'aqua', 'dodgerblue', 'yellowgreen', 'saddlebrown', 'firebrick', 'darkorange', 'sienna', 'indianred']
    markers = ['o', 'x', 'X', 'd', 'p', '*', '+', '1', '^']

    x_axis_dates = plotting_settings['x_axis_dates']
    y_axis_counts = plotting_settings['y_axis_counts']
    term = plotting_settings['term']
    distinct_dates = plotting_settings['distinct_dates']
    output_file = plotting_settings['output_file']
    plt.xticks(range(1, len(distinct_dates) + 1), distinct_dates)

    plt.title("TERM: %s" % term)
    plt.plot(x_axis_dates, y_axis_counts, marker=random.choice(markers), linestyle='dashed', label=term, color=random.choice(colours), markersize=10)
    plt.legend()
    print(">> Done plotting [%s]. Output image can be found in [%s]" % (term, output_file))
    plt.savefig(output_file)


def get_country_tweet_nr(df, country, date_in, topic):
    df.createOrReplaceTempView("tweet_data")
    tweets_count_df = spark.sql(
        """select date, topic, location, location_original, tweet_id from tweet_data where location LIKE '%{country}%' 
        and date='{date_in}' and topic LIKE '%{topic}%' """.format(country=country.lower(),
                             date_in=date_in,
                             topic=topic))
    tweets_count_df.show()
    return tweets_count_df