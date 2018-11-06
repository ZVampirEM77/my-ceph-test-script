import sys
import boto3
import json
import getopt
from botocore.client import Config

def get_bucket_policy(client, bucket):
    return client.get_bucket_policy(Bucket = bucket)

def put_bucket_policy(client, bucket, effect):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'emtest01',
            'Effect': '%s' % (effect),
            'Principal': {"AWS": ["arn:aws:iam:::user/em_test2"]},
            'Action': ['s3:GetObject', 's3:ListBucket', 's3:DeleteBucket'],
            'Resource': ["arn:aws:s3:::%s/*" % (bucket),
                         "arn:aws:s3:::%s" % (bucket)]
        }]
    }

    bucket_policy = json.dumps(bucket_policy)

    return client.put_bucket_policy(Bucket = bucket, Policy = bucket_policy)

def delete_bucket_policy(client, bucket):
    return client.delete_bucket_policy(Bucket = bucket)


def test_put(client, bucket, effect):
    put_res = put_bucket_policy(client, bucket, effect)
    print put_res

    bucket_policy = get_bucket_policy(client, bucket)
    print bucket_policy


def test_delete(client, bucket):
    delete_res = delete_bucket_policy(client, bucket)
    print delete_res

    bucket_policy = get_bucket_policy(client, bucket)
    print bucket_policy


def main():
    s3client = boto3.client('s3', endpoint_url = 'http://127.0.0.1:8000', \
                            aws_access_key_id = 'em_test1', \
                            aws_secret_access_key = 'em_test1', \
                            config = Config(signature_version = 's3v4'))

    opts, args = getopt.getopt(sys.argv[1:], 'p:d:g:n:', ['put=', 'del=', 'get=', 'deny='])
    if opts:
        for o, a in opts:
            if o in ('-p', '--put'):
                test_put(s3client, a, 'Allow')
            elif o in ('-n', '--deny'):
                test_put(s3client, a, 'Deny')
            elif o in ('-d', '--del'):
                test_delete(s3client, a)
            elif o in ('-g', '--get'):
                res = get_bucket_policy(s3client, a)
                print res

    else:
        print 'Error Option!'
        return -1

    return 0

if __name__ == '__main__':
    main()
