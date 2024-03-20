import os
import requests
import shutil
import pandas as pd

_url = "https://projects.fivethirtyeight.com/polls-page/data/president_polls.csv"
_filename = "pres_polls_2024.csv"
_destination = "/Users/mattg/Personal Projects/2024_forecast/Data/"

def fix_dates(date_str):
    try:
        return pd.to_datetime(date_str, format='%m/%d/%y')
    except ValueError:
        return pd.to_datetime(date_str, errors='coerce')

def clean_polling():
    _file_path = _destination + _filename
    _df = pd.read_csv(_file_path)
    columns_to_fix = ['start_date', 'end_date', 'election_date']

    for col in columns_to_fix:
        _df[col] = _df[col].apply(fix_dates)
        _mask = _df[col].dt.year < 2000 # assuming all dates after 2000 are valid
        _df.loc[_mask, col] = _df.loc[_mask, col].apply(lambda x: x.strftime('%m/%d/%y') if pd.notnull(x) else x)
    _df.to_csv(_destination + "pres_polls_2024_clean.csv", index=False)

def download_files():
    response = requests.get(_url)
    if response.status_code == 200:
        with open(_filename, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully")

        # move file to destination and replace if it exists
        _destination_file_path = os.path.join(_destination, _filename)
        shutil.move(_filename, _destination_file_path)
        print("File moved to:", _destination_file_path)
    else:
        print("File failed to download")

    clean_polling()
    return

download_files()
