import boto3
import os
from PIL import Image
from io import BytesIO
from project.server import app
from flask import Response
from flask import send_from_directory

def download_file(image_id):


    return send_from_directory('/home/yoann/Downloads/',
                                   'Image1.png')

    '''
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('API_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('API_AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-2'
    )
    bucket_name = 'macula-ai'
    key = 'semi-conductors/data_SC/CAM1/Inference_images/Broken_Leg_1.JPG'
    file = s3.get_object(Bucket=bucket_name, Key=key)['Body'].read()
    return Image.open(BytesIO(file))
    '''
    '''
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=test.txt"}
    )
    '''
    '''
    return s3.generate_presigned_url('get_object',
                                  Params={'Bucket': bucket_name, 'Key': key},
                                  ExpiresIn=60)
    # return s3.download_file(Bucket=bucket_name, Key=key, Filename='filenae')
    '''

'''
def download_file(region_name, bucket_name, key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=config.API_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.API_AWS_SECRET_ACCESS_KEY,
        region_name=region_name,
        config=Config(signature_version='s3v4')
    )
    return s3.get_object(Bucket=bucket_name, Key=key).get('Body')

'''