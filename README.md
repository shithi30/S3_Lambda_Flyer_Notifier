Script(s) in this repository: 
  - Pushes regular flyer data as .parquet blobs to S3 buckets, for detection and notification of new items/flyers
  - Crawls and transforms newly pushed S3 objects using Glue jobs, and shows daily statistics on GSheet from S3
  
Tech Stack: ```AWS - S3, Glue, Lambda, CloudWatch, boto3``` ```PySpark``` ```Parquet``` ```GSheets API``` ```GitHub Actions``` <br>

#### Output Notifications
<img width="380" src="https://github.com/user-attachments/assets/755b9487-aad9-46f9-919b-3b5b76854934"><br>

#### Real Time Stats - Published from [GSheet](https://docs.google.com/spreadsheets/d/1Fokcum9d__mAxw8PEN_djL34UL9l5Uq8j5LCPwjAE9Y/edit?gid=1816179544#gid=1816179544)
<img width="520" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRVmCh49pbO8q8NMLvlpyMCw3jQPiMK7wB0koHn98SlGQR3iOzuSlpiinTBeXOOP_O2CUwqD7K5lStu/pubchart?oid=377874331&format=image"><br>

Find the repository extracting daily flyers' data from top-10 ON grocers, [here](https://github.com/shithi30/Canada_Grocery_Flyer_Analytics).
