import sys
sys.path.append("/Users/gajdulj/Dev/data_engineering/")
import pandas as pd
import pytest
import tweepy_functions
import numpy as np

# Test removing Jack and adding Edward
example_df = pd.DataFrame({'is_following': ['Raphael', 'Donatello', 'Jakub','Jack'],
                   'user': ['elonmusk', 'elonmusk', 'elonmusk','elonmusk']})

example_changed_df = pd.DataFrame({'is_following': ['Raphael', 'Donatello', 'Jakub', 'Edward'],
                   'user': ['elonmusk', 'elonmusk', 'elonmusk','elonmusk']})

# doubled primary key
example_invalid_df = pd.DataFrame({'is_following': ['Raphael', 'Raphael', 'Jakub', 'Jakub'],
                   'user': ['elonmusk', 'elonmusk', 'elonmusk','elonmusk']})

# null values
example_invalid_df2 = pd.DataFrame({'is_following': [np.nan, 'Raphael', np.nan, 'Jakub'],
                   'user': ['elonmusk', 'elonmusk', 'elonmusk','elonmusk']})

@pytest.mark.parametrize("example_df, example_changed_df", [(example_df, example_changed_df)])
def test_check_new_friends(example_df, example_changed_df):

    changes = tweepy_functions.check_new_friends(username="elonmusk",
    old_snapshot=example_df, new_snapshot=example_changed_df)

    # Check number of changes detected
    assert changes.count()[0]==2

    # check for any unexpected value in account following
    assert (changes['account_following']!='elonmusk').sum() ==0

    added = changes.loc[changes['account_followed']=='Edward']['follow_action']=='added'
    assert added.sum() ==1

    removed = changes.loc[changes['account_followed']=='Jack']['follow_action']=='removed'
    assert removed.sum() ==1

@pytest.mark.parametrize(
    "example_df, example_changed_df, example_invalid_df, example_invalid_df2", 
    [(example_df, example_changed_df, example_invalid_df, example_invalid_df2)])
def test_check_if_valid_data(example_df, example_changed_df, example_invalid_df, example_invalid_df2):

    assert tweepy_functions.check_if_valid_data(example_df, primary_key='is_following')==1
    assert tweepy_functions.check_if_valid_data(example_changed_df, primary_key='is_following')==1

    assert tweepy_functions.check_if_valid_data(pd.DataFrame({'empty' : []}), primary_key='is_following')==0
    
    exceptions =[]
    try:
        tweepy_functions.check_if_valid_data(example_invalid_df, primary_key='is_following')
    except:
        exceptions.append(1)

    try:
        assert tweepy_functions.check_if_valid_data(example_invalid_df2, primary_key='is_following')==0
    except:
        exceptions.append(1)

    assert np.sum(exceptions) == 2