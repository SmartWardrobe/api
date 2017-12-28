import os
import boto3
import botocore
from botocore.client import Config

BUCKET_NAME = os.environ.get("BUCKET_NAME")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")

S3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

def upload_pic_to_s3_bucket(data, filename):
    S3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)

def download_pic_in_s3_bucket(filename):
    try:
        S3.Bucket(BUCKET_NAME).download_file(filename, 'uploads/' + filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("We dont know: ", e)
            raise

def get_bucket_list_in_s3():
    """
        Get bucket list in s3
    """
    bucket_names = []
    for bucket in S3.buckets.all():
        bucket_names.append(bucket.name)

    return bucket_names

def get_file_list_in_s3_bucket():
    """
        Get file list in s3 bucket
    """
    object_list = []
    bucket = S3.Bucket(BUCKET_NAME)
    for obj in bucket.objects.all():
        object_list.append(obj.key)

    return object_list
