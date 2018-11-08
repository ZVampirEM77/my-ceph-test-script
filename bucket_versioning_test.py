import sys
import boto3
import json
import getopt
import datetime
from botocore.client import Config


def get_bucket_versioning(client, bucket):
    return client.get_bucket_versioning(Bucket = bucket)

def put_bucket_versioning(client, bucket):
    return client.put_bucket_versioning(Bucket = bucket,
                                        VersioningConfiguration = {
                                            'Status': 'Enabled'})

def suspend_bucket_versioning(client, bucket):
    return client.put_bucket_versioning(Bucket = bucket,
                                        VersioningConfiguration = {
                                            'Status': 'Suspended'})

def list_object_versions(client, bucket):
    return client.list_object_versions(Bucket = bucket)

def remove_specified_version_obj(client, bucket, obj, version_id):
    return client.delete_object(Bucket = bucket,
                                Key = obj,
                                VersionId = version_id)

def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()

def json_format(res):
    if type(res) == str:
        res = json.loads(res)
    return json.dumps(res, indent = 4, default = default)


def main():
    s3client = boto3.client('s3', endpoint_url = 'http://192.168.2.17:8080',
                            aws_access_key_id = 'em_test1',
                            aws_secret_access_key = 'em_test1',
                            config = Config(signature_version = 's3v4'))

    opts, args = getopt.getopt(sys.argv[1:], 'g:p:s:l:d', ['get=', 'put=', 'susp=', 'list='])
    if opts:
        for o, a in opts:
            if o in ('-g', '--get'):
                res = get_bucket_versioning(s3client, a)
                print json_format(res)
            elif o in ('-p', '--put'):
                put_bucket_versioning(s3client, a)
                res = get_bucket_versioning(s3client, a)
                print json_format(res)
            elif o in ('-s', '--susp'):
                suspend_bucket_versioning(s3client, a)
                res = get_bucket_versioning(s3client, a)
                print json_format(res)
            elif o in ('-l', '--list'):
                res = list_object_versions(s3client, a)
                print json_format(res)
            elif o == '-d':
                bucket = args[0]
                obj = args[1]
                version_id = args[2]
                res = remove_specified_version_obj(s3client, bucket, obj, version_id)
                print json_format(res)

    else:
        print 'Get optional error!'
        return -1

    return 0


if __name__ == '__main__':
    main()
