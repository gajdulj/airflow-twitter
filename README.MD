### Twitter scraper- identify changes in the list of followers for a given account.


### Setup steps:
0. Get twitter api keys and save them as credentials.py in the main folder
import os
os.environ["API_KEY"]="asdjfnasjvnasjl23413241"
...

1. Create python virtual environment, install requirements
>>> make all

2. Activate the venv
cd /Users/gajdulj/Dev/data_engineering
source .venv/bin/activate

3. Initialise airflow db
>>> airflow db init

4. Create airflow credentials
airflow users create \
    --username admin \
    --firstname name \
    --lastname surname \
    --role Admin \
    --email email@gmail.com

5. Setup a webserver and scheduler
airflow webserver --port 8080
airflow scheduler

6. to run script outside dag:
python check_followers.py --user_to_check="elonmusk" --output_path="/Users/gajdulj/Dev/data_engineering/data_store/"

7. to test:
pytest -v