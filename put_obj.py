import boto3
from botocore.client import Config
import requests
from requests_aws4auth import AWS4Auth

def put_obj(bucket, obj):
    authv4 = AWS4Auth('emtest1', 'emtest1', 'us-east-1', 's3', include_hdrs='x-amz-meta-umstor-activating')
    url = 'http://192.168.2.17:7778/' + bucket + '/' + obj
    fhandle = open('acl_test.py', 'r')
    req_data = fhandle.read()
    req_headers = {'x-amz-meta-umstor-activating': 'true'}
    res = requests.put(url, headers = req_headers, data = req_data, auth = authv4)
    print res.status_code
    print res.request.headers
    print res.text


#    return client.put_object(Bucket = bucket, Key = obj, Metadata = {'x-amz-meta-umstor-activating': 'true'})

if __name__ == '__main__':
#    s3_client = boto3.client('s3', endpoint_url = 'http://192.168.2.17:7778', 
#                              aws_access_key_id = 'emtest1',
#                              aws_secret_access_key = 'emtest1',
#                              config = Config(signature_version = 's3v4'))
    put_obj("mqtest1", "acl_test.py")
#    print res
