from twitter import TwitterCrawler, TwitterReader
from preprocessor import Preprocessor
from utils import list_of_n_dates_from, write_to_csv
from stats import generate_x_and_y_values, plot, generate_slopes
import logging
from pyspark.sql import SparkSession

logger = logging.Logger(__name__)


def prompt_twitter_crawler():
    print(">> Enter key words for tweet fetching: ")
    topic = input()

    print("Enter (1) to fetch tweets for a date or (2) for date range..")
    choice = input()
    date = start_date = end_date = ""
    if choice == str("1"):
        print(">> Enter date in the form 2020-02-16 for yyyy-MM-dd: ")
        date = input()
        # TODO: test if entered value is date
    elif choice == str("2"):
        print(">> Enter start_date in the form 2020-02-16 for yyyy-MM-dd: ")
        start_date = input()
        # TODO: test if entered value is date
        print(">> Enter end_date in the form 2020-02-24 for yyyy-MM-dd: ")
        end_date = input()
    else:
        raise AttributeError("invalid input, enter 1 or 2.")

    print(">> Enter country or leave blank for netherlands: ")
    country = input().lower() if input() != '' else 'netherlands'

    settings = {
        "country": country,
        "topic": topic,
        "tweets_nr": 200,
        "file_path": "data/TwitterData/twitter-sample.json",
        "creds_file_name": "twitter_ani.json"
    }

    return settings


def process(df, date, inp_col, outp_col, term):
    # TODO: add all the preprocessing steps here to avoid redundancy, if there's time left
    return df


def prompt_for_input():
    print(">> Enter key words for tweet fetching: ")
    topic = input()

    print(">> Enter relative path for the data file: e.g. data/TwitterData/myfile.json")
    data_file_path = input()

    print(">> Enter credentials file name, after placing it into the vault/ dir. Press enter to skip.")
    creds_path = input()

    print(">> Enter date before 2012-01-08 in the same format yyyy-MM-dd: ")
    date = input()

    print(">> Enter delta int between 1 and 7 for how many days data will be fetched: ")
    delta_days = input()

    print(">> Enter file name for output with .csv extension: ")
    oFile_name = input()

    print(">> Enter language (\'english\', \'dutch\'.. leave empty for dutch): ")
    lang = input()

    settings = {
        "user_topic": topic,
        "file_path": data_file_path,
        "creds_file_name": creds_path,
        "start_date": date,
        "delta_days": delta_days,
        "output_file_name": oFile_name,
        "lang": lang
    }

    return settings


def main():

    settings = {
        "user_topic": "egel in tuin",
        "file_path": "data/2020_03_15_13.json",
        "creds_file_name": "twitter_ani.json",
        "start_date": "2020-03-15",
        "delta_days": 5,
        "output_file_name": "output_res.csv",
        "lang": "english"
    }

    # settings = prompt_for_input()

    if not settings['output_file_name'].endswith('.csv'):
        raise AttributeError("It seems the output file is missing .csv extension. Please add it.")

    # if settings['creds_file_name'] is not None:
    #     if not settings['creds_file_name'].endswith('.json'):
    #         raise AttributeError("It seems the twitter creds file is missing .json extension. Please add it.")

    # if settings['start_date'] != "2012-01-08" and settings['start_date'] not in list_of_n_dates_from("2012-01-08", 7):
    #     raise KeyError("The provided start date is not in the dataset. "
    #                    "Please modify the date with 2012-01-08 or up to 7 days earlier but then modify also delta_days "
    #                    "to be not more than 2012-01-08 - 7 days., e.g. if date provided is 2012-01-08, "
    #                    "delta can be up to 7, with 2012-01-06 - up to 5 etc. Otherwise there won't be any data.")

    reader = TwitterReader(**settings)
    df = reader.read()
    preprocessor = Preprocessor(df, lang="dutch")
    start_date = settings.get('start_date')
    date_list = list_of_n_dates_from(start_date, 5)
    trends_from_all_days = dict()
    for day in date_list:
        print(">> Fetching data for [%s]" % day)
        filtered_df = reader.get_filtered_data_by_date(day)
        reader.count_records(filtered_df)
        filtered_df = preprocessor.normalize(df=filtered_df, inp_col='content', outp_col='content')
        filtered_df = preprocessor.remove_special_chars(df=filtered_df, inp_col='content', outp_col='content')
        filtered_df = preprocessor.tokenize(df=filtered_df, inp_col='content', outp_col='content_words')
        filtered_df = preprocessor.remove_stopwords(df=filtered_df, inp_col='content_words', outp_col='sw_removed')
        # NB! TF-IDF also works, but is not used here, instead I get top terms with the get_most_frequest_terms() method
        # Get occurrences of the provided terms
        query = settings.get('user_topic')
        query_term_split = query.split()
        res_user_query = preprocessor.count_term_occurences(df=filtered_df, term_list=query_term_split, col_name='content')
        print(">> Tweets containing all provided terms from the query for [%s]: [%s]" % (day, res_user_query))
        write_to_csv(file_name=settings['output_file_name'], topic=query, date=day, count=res_user_query)

        top_trend_for_date = preprocessor.get_top_trends(df=filtered_df, inp_col='sw_removed')
        print(">> Top trends for %s: %s" % (day, top_trend_for_date))
        trends_from_all_days.update(top_trend_for_date)
        print("=" * 200 + "\n")

    # Now we have a list of trends, let's look them up and add to the data
    trends_from_all_days = sorted(trends_from_all_days.items(), key=lambda x: x[1], reverse=True)
    trends_list = [item[0] for item in trends_from_all_days]
    print("=== Fetching top trending tweets ===")
    for day in date_list:
        day_tweets_df = reader.get_filtered_data_by_date(day)
        reader.count_records(day_tweets_df)
        day_tweets_df = preprocessor.normalize(df=day_tweets_df, inp_col='content', outp_col='content')
        day_tweets_df = preprocessor.remove_special_chars(df=day_tweets_df, inp_col='content', outp_col='content')
        day_tweets_df = preprocessor.tokenize(df=day_tweets_df, inp_col='content', outp_col='content_words')
        day_tweets_df = preprocessor.remove_stopwords(df=day_tweets_df, inp_col='content_words', outp_col='sw_removed')

        for term in trends_list:
            res_top_trends = preprocessor.count_term_occurences(df=day_tweets_df, term_list=term, col_name='content')
            print(">> Tweets containing term [%s] for [%s]: [%s]" % (term, day, res_top_trends))
            write_to_csv(file_name=settings['output_file_name'], topic=term, date=day, count=res_top_trends)

    plt, plotting_settings = generate_x_and_y_values(file_path='output/'+settings['output_file_name'])
    generate_slopes([item.pop('paired_data') for item in plotting_settings])

    for item in plotting_settings:
        print(">> Plotting tweet data")
        plot(plt, **item)


if __name__ == '__main__':
    main()
