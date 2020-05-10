import twitter

settings = {
    "user_topic": "egel in tuin",
    "file_path": "data/TwitterData/twitter-sample.json",
    "creds_file_name": "twitter_ani.json",
    "start_date": "2012-01-08",
    "delta_days": 5,
    "output_file_name": "output_res.csv"
}


def test_cols_filtered_correctly():
    reader = twitter.TwitterReader(**settings)
    filtered_df = reader.get_filtered_data_by_date('2012-01-08')
    col_list = ['tweet_id',
                'day_created'
                'day_query'
                'content'
                'username'
                'user_id'
                'followers_coun'
                'statuses_coun'
                'type'
                'language'
                'location']

    for col in filtered_df.columns:
        assert col in col_list

