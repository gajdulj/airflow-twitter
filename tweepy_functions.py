import tweepy, os
import pandas as pd

def authenticate_tweepy(api_key, api_secret, access_token, token_secret):
    """
    Authenticate the connection to twitter API with access keys.
    """
    auth = tweepy.OAuthHandler(api_key, api_secret)
    
    auth.set_access_token(access_token, token_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True,timeout=500)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
        
    return api

def user_info(api, nickname):
    user = api.get_user(nickname)
    print("User details:")
    print(user.name)
    print(user.description)
    print(user.location)
    
def snapshot_friends(api,username):
    
    # friends = accounts followed by user.
    friends = []
    # getting list of people followed by user. Latest first.
    for friend in tweepy.Cursor(api.friends, username).items():
        friends.append(friend.screen_name)
    print(f"Identified {len(friends)} friends for {username}.")
    
    d = {'is_following': friends}
    df = pd.DataFrame(data=d)
    df['user'] = username
    
    return df

def check_if_valid_data(df: pd.DataFrame, primary_key: str) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("Empty dataframe passed. Finishing execution")
        return False 

    # Primary Key Check
    if pd.Series(df[primary_key]).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    print("Snapshot data validation went well.")
    return True

def check_diff(TableA,TableB,column):
    # Identify what values are in TableB and not in TableA
    key_diff = set(TableB[column]).difference(TableA[column])
    where_diff = TableB[column].isin(key_diff)

    # Slice TableB accordingly and append to TableA
    # TableA.append(TableB[where_diff], ignore_index=True)
    return key_diff

def check_new_friends(username, old_snapshot, new_snapshot):
    """
    snapshot = last point in time saved.
    friends = latest list of friends.
    
    Expects two dataframes with the same columns.
    Checks for new & removed records in dataframe.
    
    # scenario 1. There are some friends that were added. 
    friends will have more records than the snapshot.
    
    friends LEFT join snapshot on "is_following".
    Any records with nulls will be the new users.
    
    # scenario 2. Some friends were removed.
    Friends will have less records than the snapshot.
    
    snapshot LEFT JOIN friends on "is_following".
    Records with nulls will be the deleted users.
    """
    # check for new entries

    new_entries = check_diff(TableA=old_snapshot,
               TableB=new_snapshot,
               column='is_following')

    # check for missing entries

    missing = check_diff(TableA=new_snapshot,
               TableB=old_snapshot,
               column='is_following')
    
    new = len(new_entries)
    deleted = len(missing)
    print(f"Found {new} new friends and {deleted} deleted friends.")
    # get results to pandas dfs
    start_follow = pd.DataFrame(new_entries,columns=['account_followed'])
    start_follow['follow_action'] = "added"

    stop_follow = pd.DataFrame(missing,columns=['account_followed'])
    stop_follow['follow_action'] = "removed"

    changes = pd.concat([start_follow, stop_follow])

    changes['account_following'] = username
    changes['time'] = pd.to_datetime('now')
    return changes

def friends_snapshot_exists(output_path,username):
    """Checks if snapshot file already exists"""
    return os.path.exists(output_path+f"{username}_friends.csv")

def changes_exists(output_path):
    """Checks if changes file already exists"""
    return os.path.exists(output_path+"changes.csv")

def reconcile_followers(api, username, output_path):
    """
    Compares the newly downloaded data with the last snapshot.
    Writes any differences to a file.
    Updates the snapshot for the account for later comparisons.
    """
    new_snapshot = snapshot_friends(api,username=username)
    check_if_valid_data(df=new_snapshot, primary_key="is_following")

    if friends_snapshot_exists(output_path=output_path, username=username):
        print("Snapshot already exists. Proceeding to comparing...")
        snapshot_old = pd.read_csv(output_path+f"{username}_friends.csv")
    else:
        print("No snapshot found.")
        new_snapshot.to_csv(output_path+f"{username}_friends.csv", header = True,index=False)
        exit()

    changes = check_new_friends(username=username, 
        old_snapshot=snapshot_old, 
        new_snapshot=new_snapshot)

    if changes_exists(output_path):
        changes.to_csv(output_path+'changes.csv', mode = 'a', header = False)
    else:
        changes.to_csv(output_path+'changes.csv', mode = 'a', header = True)

    # update the old snapshot stored for future comparisons
    new_snapshot.to_csv(output_path+f"{username}_friends.csv", header = True,index=False)