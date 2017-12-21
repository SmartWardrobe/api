import os
import boto3
import botocore
from botocore.client import Config

BUCKET_NAME = os.environ.get("BUCKET_NAME")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")

s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
)

def upload_pic_to_s3_bucket(data, filename):
    s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)

def download_pic_in_s3_bucket(filename):
    try:
        s3.Bucket(BUCKET_NAME).download_file(filename, 'pics/' + filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("We dont know: ", e)
            raise