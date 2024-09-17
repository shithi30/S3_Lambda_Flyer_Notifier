# import
import os
import boto3
import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd
from datetime import datetime

# AWS artifacts
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
s3 = boto3.client("s3")

# GSheet artifacts
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(json.loads(os.getenv("READ_WRITE_TO_GSHEET_APIS_JSON")), scopes = scope)
client = gspread.authorize(creds)

# today's data
sheet_link = "https://docs.google.com/spreadsheets/d/1Fokcum9d__mAxw8PEN_djL34UL9l5Uq8j5LCPwjAE9Y/edit?usp=sharing"
sheet_name = "All Items"

# retrieve data
spreadsheet = client.open_by_url(sheet_link)
worksheet = spreadsheet.worksheet(sheet_name)
flyer_df = pd.DataFrame(worksheet.get_all_records()).replace("", None)

# to parquet
filename = "grocery_flyer_items_" + datetime.now().strftime("%Y-%m-%d") + ".parquet"
flyer_df.to_parquet(filename, index = False)

# upload blob
response = s3.upload_file(filename, "daily-parquet-flyers", filename)
