import tweepy as tw
import json, traceback, csv
from datetime import datetime
from utils import country_list
from preprocessor import Preprocessor
from pyspark.sql import SparkSession


class TwitterCrawler(object):
    def __init__(self, **kwargs):
        self.path = 'vault/' + kwargs.get('creds_file_name')
        self.topic = kwargs.get('topic')
        self.tweets_nr = kwargs.get('tweets_nr', '')
        self.country = kwargs.get('path')

        self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET, self.API_KEY, self.API_SECRET_KEY = self._get_creds(self.path)
        self.api = self.authenticate()
        self.raw_tweet_list = list()
        self.full_trends_dict = dict()
        self.preprocessor = Preprocessor()
        self.tweets_nr = self.tweets_nr if self.tweets_nr else 200

    def update_topic(self, new_topic):
        """ Update the topic so that one can fetch more tweets with a new topic

        :param new_topic: new topic to replace the old one with
        :type new_topic: str
        """
        self.topic = new_topic

    def _get_creds(self, path):
        with open(path, 'r') as file:
            creds = json.load(file)
        return creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'], creds['API_KEY'], creds['API_SECRET_KEY']

    def authenticate(self):
        auth = tw.OAuthHandler(self.API_KEY, self.API_SECRET_KEY)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)
        return api

    def save_to_csv(self, file_name, tweets, date_in):
        """ Save a list of tweets as a CSV file, adding header and all

        :param file_name: file name. it will always be saved in the data/ folder
        :type file_name: str

        :param tweets: list of tweets to save to the file
        :type tweets: list

        :param date_in: date for which to fetch the tweets
        :type date_in: str for the date of format "yyyy-MM-dd"

        :return:
        """
        path = 'data/'+file_name+'.csv'.lower().strip()
        headers = ["tweet_id", "date", "topic", "location","location_original", "user", "fav_nr", "tweet_text"]

        with open(path, 'a') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=headers)

            if csvFile.tell() == 0:
                print(">> Creating a new file [{}].. and adding header".format(path))
                writer.writeheader()
            else:
                print(">> File [{}] already exists. Appending data to it..".format(path))

            for tweet in tweets:
                location_orig = tweet.author.location.lower()
                location = tweet.author.location.lower() if tweet.author.location.lower() else "unknown"
                if len(location.split()) > 0 and location != "unknown":
                    location = self.preprocessor.clean_up(location)
                writer.writerow(
                    {"tweet_id": tweet.id,
                     "date": date_in,
                     "topic": self.topic,
                     "location": location,
                     "location_original": location_orig,
                     "user": tweet.user.screen_name,
                     "fav_nr": tweet.favorite_count,
                     "tweet_text": "{}".format(tweet.full_text).replace("\n", " ").replace("\r", " ")})

    def get_trends_list(self, country):
        """ Fetch a full list of trending topics for a given country at that point in time.

        :param country: Country for which to fetch the trending topic
        :type country: str

        :return: list of trends, sorted in DESC order, so the most popular topic is at index 0
        """
        if not country:
            raise AttributeError("Country must be provided.")

        trends_list = dict()
        if country.lower() in country_list().keys():
            WOE_ID = country_list().get(country.lower())
            print(">> Found WOEID for {} = {}".format(country, WOE_ID))
            country_trends = self.api.trends_place(WOE_ID)
            trends = json.loads(json.dumps(country_trends, indent=1))
            for trend in trends[0]["trends"]:
                if trend['tweet_volume'] != None:
                    trends_list.update({trend['name']: trend['tweet_volume']})

            trends_list = sorted((value, key) for (key, value) in trends_list.items())
            trends_list = trends_list[::-1]
        else:
            raise KeyError("WOEID not found for %s in the country list file. Please make sure you are spelling it correctly and double check \"woeid/countries.json\" for the id." % country)
        return trends_list

    def get_top_trend(self, country):
        """ Get top 1 trending topic for a given country at this point in time

        :param country: Country for which to fetch the trending topic
        :type country: str

        :return: str of the topic
        """
        trends_list = self.get_trends_list(country)
        top_trend = trends_list[0]
        print(">> Top 1 trending topic for {}: << {} >>".format(country.upper(), top_trend[1]))
        return top_trend

    def fetch_raw_tweets(self, start_date):
        """ Fetch raw tweets from twitter for a given term

        The term is assigned upon object initiation and has a method to overwrite it, if necessary

        :param date_in: date for which to fetch the tweets
        :type date_in: str for the date of format "yyyy-MM-dd"

        :return: list of raw tweets fetched from the "Status" object returned by the API
        """
        start_date_in = start_date
        start_date = datetime.strptime(start_date_in, "%Y-%m-%d")
        end_date = datetime.strptime(start_date_in+" 23:59:59", "%Y-%m-%d %H:%M:%S")

        print(">> Fetching data for: topic=[{}] - date=[{}] - nr_of_tweets=[{}]".format(self.topic, start_date, self.tweets_nr))
        tweets = tw.Cursor(self.api.search,
                           q="{} -filter:retweets".format(self.topic),
                           lang="en",
                           since="{}".format(start_date),
                           tweet_mode='extended').items(self.tweets_nr)

        self.raw_tweet_list = [tweet for tweet in tweets if start_date < tweet.created_at < end_date]
        return self.raw_tweet_list


class TwitterReader(object):
    def __init__(self, **kwargs):
        self.path = kwargs.get('file_path')
        self.ext = self.path.split('.')[-1]
        self.header = kwargs.get('header', None)

        try:
            self.spark = SparkSession.builder.appName("twitter_reader").getOrCreate()
        except Exception:
            traceback.print_exc()
        self.template = """df = self.spark.read.{ext}("{file}"{header})""".format(ext=self.ext,
                                                                                  file=self.path,
                                                                                  header=", header={}".format(self.header) if self.header else "")

    def read(self):
        print(">> Reading the provided file..")
        if self.ext == "csv" and not self.header:
            df = self.spark.read.csv(self.path)
        elif self.ext == "csv" and self.header:
            df = self.spark.read.csv(self.path, header=True)
        elif self.ext == "json":
            df = self.spark.read.json(self.path)
        else:
            raise AttributeError("File with unsupported extension provided. Please provide path to json or csv file.")
        self.df = df
        return self.df

    def extract_cols(self, df, col_list, filter=None, rem_retweets=None):
        print(">> Column list provided: [%s]" % col_list)
        rem_retweets_filter = "" if not rem_retweets else "text ! like '%RT%'"

        df.createOrReplaceTempView("tweets_df")
        query_template = """SELECT {col_list} FROM tweets_df {filter} {retweets}""".format(
            col_list=col_list,
            filter="WHERE {}".format(filter) if filter else "",
            retweets = "WHERE {}".format(rem_retweets_filter) if not filter else "AND {}".format(rem_retweets_filter) if filter else ""
        )

        print(">> QUERY: %s" % query_template)
        filtered_df = self.spark.sql(query_template)
        filtered_df.show(10, False)
        return filtered_df

    def get_filtered_data_by_date(self, date):
        self.df.createOrReplaceTempView('raw_data')
        df_by_day_query = """
            SELECT * FROM
                (SELECT
                    a.tweet_id,
                    CAST(to_date(a.created_at) AS STRING) as day_created,
                    CAST("{day}" AS STRING) as day_query,
                    a.content,
                    a.username, 
                    a.user_id,
                    a.followers_count,
                    a.statuses_count,
                    a.type, 
                    a.language, 
                    a.location
                FROM (select    interaction.id as tweet_id, 
                                from_unixtime(unix_timestamp(interaction.created_at, 'EEE, dd MMM YYYY HH:mm:ss ZZZZ')) as created_at,
                                interaction.author.username, 
                                interaction.content, 
                                interaction.type, 
                                language.tag as language, 
                                twitter.user.location,
                                twitter.user.followers_count,
                                twitter.user.id as user_id,
                                twitter.user.statuses_count
                      from      raw_data) a
                ) b
            WHERE b.day_created=b.day_query
            AND b.content ! LIKE '%RT%'
            """
        print(">> Fetching the columns needed from the twitter data.")
        query = df_by_day_query.format(day=date)
        filtered_df = self.spark.sql(query)
        return filtered_df

    def count_records(self, df):
        print(">> Counting the data..")
        df.createOrReplaceTempView("day_by_day_res")
        df_count_data = self.spark.sql("""SELECT count(1) as nr_of_records FROM day_by_day_res""")
        data_count = df_count_data.select("nr_of_records").collect()
        data_count = [row['nr_of_records'] for row in data_count]
        data_count = data_count[0]
        print(">> [%d] tweets found for this day." % data_count)