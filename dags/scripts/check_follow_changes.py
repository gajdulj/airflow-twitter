import argparse, os
import sys
sys.path.append("/Users/gajdulj/Dev/data_engineering/")
import tweepy_functions as tpy
import credentials # When imported, populates env variables.

def check_follow_changes(**kwargs):
    API_KEY = os.environ["API_KEY"]
    API_SECRET = os.environ["API_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    TOKEN_SECRET = os.environ["TOKEN_SECRET"]

    api = tpy.authenticate_tweepy(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        token_secret=TOKEN_SECRET
        )

    tpy.reconcile_followers(api, 
        username=kwargs['user_to_check'], 
        output_path=kwargs['output_path'])

