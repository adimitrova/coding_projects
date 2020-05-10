from pyspark.ml.feature import Tokenizer, RegexTokenizer, StopWordsRemover, NGram, StringIndexer, HashingTF, IDF
from pyspark.sql import readwriter, functions as fn
from pyspark.sql.types import IntegerType
from pyspark.sql import SparkSession
import nltk, math, json
from utils import country_list, city_list
from collections import Counter, defaultdict


class Preprocessor(object):
    # TODO: make it use self.df for the whole processing by setting a df in the init method
    # TODO: make the DF get updates after every transformation instead of methods being static
    def __init__(self, df, lang):
        self.spark = SparkSession.builder.appName("twitter_stuff").getOrCreate()
        self.df = df
        print(">> The provided df has the following schema: ")
        self.df.printSchema()
        print(">> The provided df has the following data: ")
        self.df.show(5)
        self.lang = lang

        nltk.download("stopwords")
        locale = self.spark._jvm.java.util.Locale
        locale.setDefault(locale.forLanguageTag("en-US"))

        self.stopwordList = nltk.corpus.stopwords.words(lang)
        if lang == "dutch":
            # Enrich th sw list with some dutch words which seem to be missing
            self.stopwordList.extend(['echt', 'wel', 'we', 'even', 'ga', 'jij', 'ff', 'x', 'n', 'haha', 'the', 'co', 'xd', 'hoor', 'net'])

        avail_languages = (
            "arabic",
            "danish",
            "dutch",
            "english",
            "finnish",
            "french",
            "german",
            "hungarian",
            "italian",
            "norwegian",
            "porter",
            "portuguese",
            "romanian",
            "russian",
            "spanish",
            "swedish",
        )

        print(">> NB! When using the stopwords remover, you can change the language by passing one of the following languages in the \'lang\' param: {} \n".format(avail_languages))

    def _mergeDict(self, dict1, dict2):
        ''' Merge dictionaries and keep values of common keys in list'''
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = [value, dict1[key]]
        return dict3

    def lemmatize(self, override_df=True):
        pass

    def tokenize(self, df, inp_col, outp_col, override_df=True):
        """ Tokenizer to split text into a list of words

        :param df:
        :type df: <class 'pyspark.sql.dataframe.DataFrame'>

        :param inp_col: Input col name which will be transformed into tokens
        :type inp_col: str

        :param outp_col: Output col name which will store the output data.
                         Could be the same col name as input col
        :type outp_col: str

        :return: a df with the output col split into words/tokens.
        """
        tokenizer = Tokenizer(inputCol=inp_col, outputCol=outp_col)
        tokenized_df = tokenizer.transform(df)
        print(">> Done [tokenize]. Updating object's df.. ")
        self.df = tokenized_df if override_df else self.df
        return tokenized_df

    def pos_tag(self, tokenized_df, override_df=True):
        pass

    def get_ngrams(self, tokenized_df, override_df=True):
        pass

    def remove_stopwords(self, df, inp_col, outp_col, override_df=True):
        """

        :param inp_col:
        :param outp_col: CANNOT be the same as inp_col
        :param lang:
        :return:
        """
        sw_remover = StopWordsRemover(inputCol=inp_col, outputCol=outp_col, stopWords=self.stopwordList)
        sw_df = sw_remover.transform(df)
        print(">> Done [remove_stopwords]. Updating object's df.. ")
        self.df = sw_df if override_df else self.df
        return sw_df

    def normalize(self, df, inp_col, outp_col, override_df=True):
        """

        :param df:
        :type df: <class 'pyspark.sql.dataframe.DataFrame'>

        :param inp_col: Input col name which will be transformed into lowercase
        :type inp_col: str

        :param outp_col: Output col name which will store the output data.
                         Could be the same col name as input col
        :type outp_col: str

        :return: a df with the output col normalized to lowercase
        """
        df = df.withColumn(outp_col, fn.lower(fn.col(inp_col)))
        print(">> Done [normalize]. Updating object's df.. ")
        self.df = df if override_df else self.df
        return df

    def string_index(self, df, input_col, output_col, override_df=True):
        pass

    def remove_special_chars(self, df, inp_col, outp_col, dnr_chars=None, override_df=True):
        """ Remove special characters and extra spaces from a column from the DF.

        :param df: dataframe
        :type df: <class 'pyspark.sql.dataframe.DataFrame'>

        :param dnr_chars: [Do-Not-Remove-chars] - list of characters to NOT be stripped from the text. By default for twitter data # and @ symbolx are omitted and left in the content of the tweet col
        :type dnr_chars: list

        :return: cleansed_df
        """
        clean_df = df.withColumn(outp_col, fn.regexp_replace(inp_col, '[^#@a-zA-Z]', ' '))
        clean_df = clean_df.withColumn(outp_col, fn.regexp_replace(inp_col, '\s\s+', ''))
        print(">> Done [remove_special_chars]. Updating object's df.. ")
        self.df = clean_df if override_df else self.df
        return clean_df

    def city_clean_up(self, text):
        """ Cleans up location string and fetches possible countries from there

        :param text: textual data for the location
        :type text: str

        :return: a string of value separated by a pipe symbol for the sake of easy querying in SQL later.
        """
        country_list = set()
        if len(text.split(",")) == 2:
            # Assumes input like "chicago, il" or "amsterdam, nl"
            given_city = text.split(",")[0]
            if len(city_list(given_city)) != 0:
                country_list = city_list(given_city)
                return '|'.join(country_list)
        elif len(text.split()) >= 2:
            for item in text.split():
                country_list.update(city_list(item))
                return '|'.join(country_list)
        else:
            return "unknown"

    def tf_idf(self, df, inp_col):
        """ Computes TF-IDF and returns the scores of the terms used
        NB: Not used in the actual solution, because I thought it will get me the right term as a str
        instead of only scores, so I use the get_most_frequest_terms() method for this, instead

        :param doc:
        :param doc:

        :param term:
        :param term:

        :param doclist:
        :param doclist:
        :return:
        """
        print("Initializing TF-IDF processing..")
        df_tf_idf = df.select(inp_col)
        hashingTF = HashingTF(inputCol=inp_col, outputCol="raw_features")

        tf = hashingTF.transform(df_tf_idf)
        # tf.show(10, False)
        # tf.printSchema()
        tf.cache()
        idf = IDF(inputCol='raw_features', outputCol='features', minDocFreq=10).fit(tf)
        tfidf = idf.transform(tf)
        tfidf.select("tf_idf", "features").show()

        idf = IDF(inputCol='rawFeatures', outputCol='features', minDocFreq=10).fit(tf)
        tfidf = idf.transform(tf)
        rescaledData = tfidf.transform(tf)

        rescaledData.select(inp_col, "features").show()
        return rescaledData

    def get_top_trends(self, df, inp_col, n=1):
        print(">> Fetching top trending topics for this day.")
        items = df.select(inp_col).collect()
        items_arr = [row[inp_col] for row in items]
        all_items = []
        for item_list in items_arr:
            for item in item_list:
                all_items.append(item)

        word_count = dict(Counter(all_items))
        # Remove all words that occur less than 10 times and with key='', i.e. with no key and items with one-letter keys
        word_count_filtered = dict(filter(lambda elem: elem[1] > 20, word_count.items()))
        word_count_filtered = dict(filter(lambda elem: elem[0] != '', word_count_filtered.items()))
        word_count_filtered = dict(filter(lambda elem: len(elem[0]) != 1, word_count_filtered.items()))

        word_count_sorted = sorted(word_count_filtered.items(), key=lambda x: x[1], reverse=True)
        top_terms = dict()
        for i in range(0, n):
            key = word_count_sorted[i][0]
            value = word_count_sorted[i][1]
            top_terms[key] = value
        return top_terms

    def count_term_occurences(self, df, term_list, col_name, date=None):
        df.createOrReplaceTempView("tweets_today")
        if isinstance(term_list, list):
            if len(term_list) > 1:
                temp_df = df
                temp_df.registerTempTable("temp_res")

                res = -1
                i = 0
                terms = [q for q in term_list if q not in self.stopwordList]

                while i < len(terms):
                    if i == 0:
                        print(">> Checking for term %s.." % (terms[i].upper()))
                        temp_df = self.spark.sql(
                            """SELECT {col} as content FROM tweets_today WHERE content LIKE '%{q}%'""".format(col=col_name, q=terms[i]))
                        i += 1
                    elif i == len(terms) - 1:
                        print(">> Checking for term %s.." % (terms[i].upper()))
                        temp_df = self.spark.sql(
                            """SELECT count(1) as count FROM temp_res WHERE content LIKE '%{q}%'""".format(q=terms[i]))
                        res = temp_df.select("count").collect()
                        res = [row['count'] for row in res]
                        res = res[0]
                        i += 1
                    else:
                        print(">> Checking for term %s.." % (terms[i].upper()))
                        temp_df = self.spark.sql(
                            """SELECT content as content FROM temp_res WHERE content LIKE '%{q}%'""".format(q=terms[i]))
                        i += 1
                res = res if res != 0 else 0
                return res
            else:
                print(">> Checking for term %s.." % (term_list[0].upper()))
                temp_df = self.spark.sql(
                    """SELECT count(1) as count FROM tweets_today WHERE content LIKE '%{q}%'""".format(q=term_list[0]))
                res = temp_df.select("count").collect()
                res = [row['count'] for row in res]
                res = res[0]
                return res
        elif isinstance(term_list, str):
            temp_df = self.spark.sql(
                """SELECT count(1) as count FROM tweets_today WHERE content LIKE '%{q}%'""".format(q=term_list))
            res = temp_df.select("count").collect()
            res = [row['count'] for row in res]
            res = res[0]
            return res
        else:
            raise AttributeError("Incorrect data type provided for term list in count_term_occurences(). Supply str or list")
