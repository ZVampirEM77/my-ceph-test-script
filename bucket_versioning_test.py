import sys
import boto3
import json
import getopt
from botocore.client import Config


def get_bucket_versioning(client, bucket):
    return client.get_bucket_versioning(Bucket = bucket)


def main():
    s3client = boto3.client('s3', endpoint_url = 'http://192.168.2.17:8080',
                            aws_access_key_id = 'em_test1',
                            aws_secret_access_key = 'em_test1',
                            config = Config(signature_version = 's3v4'))

    opts, args = getopt.getopt(sys.argv[1:], 'g:', ['get='])
    if opts:
        for o, a in opts:
            if o in ('-g', '--get'):
                res = get_bucket_versioning(s3client, a)
                print res
    else:
        print 'Get optional error!'
        return -1

    return 0


if __name__ == '__main__':
    main()