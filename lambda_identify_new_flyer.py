# import
import boto3
import io
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os
import json

# execution logic
def lambda_handler(event, context):
    
    # client
    s3 = boto3.client("s3", region_name = "ca-central-1")
    
    # yesterday's flyer
    past_flyer_pq = "grocery_flyer_items_" + (datetime.today() - timedelta(days = 1)).strftime("%Y-%m-%d") + ".parquet"
    past_flyer_obj = s3.get_object(Bucket = "daily-parquet-flyers", Key = past_flyer_pq)
    past_flyer_df = pd.read_parquet(io.BytesIO(past_flyer_obj["Body"].read()))
    
    # today's flyer
    present_flyer_pq = "grocery_flyer_items_" + datetime.today().strftime("%Y-%m-%d") + ".parquet"
    present_flyer_obj = s3.get_object(Bucket = "daily-parquet-flyers", Key = present_flyer_pq)
    present_flyer_df = pd.read_parquet(io.BytesIO(present_flyer_obj["Body"].read()))
    
    # changes
    today_counts = (present_flyer_df.groupby("platform").size().reset_index(name = "items_today"))
    yesterday_counts = (past_flyer_df.groupby("platform").size().reset_index(name = "items_yesterday"))
    merged_df = pd.merge(today_counts, yesterday_counts, on = "platform")
    change_df = merged_df[merged_df["items_today"] != merged_df["items_yesterday"]]
    
    # email - from, to, body
    sender_email = "shithi30@gmail.com"
    receiver_email = ["shithi30@outlook.com"]
    body = '''
    Grocers have items added/deducted on flyers today.<br><br>
    ''' + change_df.to_html(index = False, justify = "center", col_space = "120px") + '''
    <br>Full list of items on today's top-10 flyers? Click <a href="https://docs.google.com/spreadsheets/d/1Fokcum9d__mAxw8PEN_djL34UL9l5Uq8j5LCPwjAE9Y/edit?usp=sharing">here</a>.<br><br>
    Thanks,<br>
    Shithi Maitra<br>
    Ex Asst. Manager, CS Analytics<br>
    Unilever BD Ltd.<br>
    '''
    
    # email - object
    html_msg = MIMEText(body, "html")
    html_msg["Subject"] = "Anything New for Grocery?"
    html_msg["From"] = "Shithi Maitra"
    html_msg["To"] = ", ".join(receiver_email)
    
    # email - send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, os.getenv("EMAIL_PASS"))
      if change_df.shape[0] > 0: server.sendmail(sender_email, receiver_email, html_msg.as_string())
    
    # log
    return {"statusCode": 200, "body": json.dumps("Lambda for reporting changes on flyers ran successfully.")}
