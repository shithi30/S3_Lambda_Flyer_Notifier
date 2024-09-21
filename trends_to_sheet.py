# import
import os
import boto3
import io
import pandas as pd
import duckdb
from googleapiclient.discovery import build
from google.oauth2 import service_account

READ_WRITE_TO_GSHEET_APIS_JSON

# env, client
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
s3 = boto3.client("s3")

# blob name - key
response = s3.list_objects_v2(Bucket = "glue-etl-summaries")
for obj in response.get("Contents", []): key = obj["Key"]

# blob to dataframe
flyer_obj = s3.get_object(Bucket = "glue-etl-summaries", Key = key)
flyer_df = pd.read_csv(io.BytesIO(flyer_obj["Body"].read()))

# summary
qry = '''
select report_date, count(distinct platform) platforms, sum(flyer_items) flyer_items
from flyer_df
group by 1
order by 1 desc
'''
summary_df = duckdb.query(qry).df()

# credentials
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("READ_WRITE_TO_GSHEET_APIS_JSON"))
SAMPLE_SPREADSHEET_ID = "1Fokcum9d__mAxw8PEN_djL34UL9l5Uq8j5LCPwjAE9Y"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# APIs
creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes = SCOPES)
service = build("sheets", "v4", credentials = creds)
sheet = service.spreadsheets()

# load
res = sheet.values().clear(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "Stats").execute()
res = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "'Stats'!A1", valueInputOption = "USER_ENTERED", body = {"values": [summary_df.columns.values.tolist()] + summary_df.values.tolist()}).execute()
