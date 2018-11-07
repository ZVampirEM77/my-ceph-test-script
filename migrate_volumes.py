import os
import sys
import json
import requests
import getopt
import subprocess

VOLUMES_V3 = 'http://12.34.56.78:8776/v3/xxxxx'
IDENTITY = 'http://12.34.56.78:5000/v2.0'
PROJECT = 'zvampirem'
USER = 'zvampirem'
PWD = 'zvampirem'
HEADERS = {'Content-Type': 'application/json'}

def get_token():
    req_url = IDENTITY + '/tokens'
    data = '{"auth": {"tenantName": "%s", "passwordCredentials": {"username": "%s", "password": "%s"}}}' % (PROJECT, USER, PWD)
    try:
        res = requests.post(req_url, data = data, headers = HEADERS)
        res = res.json()
    except Exception as e:
        print e
        return ''

    token = res['access']['token']['id']
    return token


def get_volumes_detail():
    req_url = VOLUMES_V3 + '/volumes/detail'
    headers = HEADERS
    token = get_token()
    if not token:
        return None
    headers['X-Auth-Token'] = token
    return requests.get(req_url, headers = headers)

def get_all_volumes():
    volumes = get_volumes_detail()['volumes']
    all_volumes = []
    for volume in volumes:
        volume_name = 'volume-' + volume['id']
        all_volumes.append(volume_name)
    return all_volumes

def get_available_volumes():
    volumes = get_volumes_detail()['volumes']
    available_volumes = []
    for volume in volumes:
        if volume['status'] == 'available' and not volume['attachments']:
            volume_name = 'volume-' + volume['id']
            available_volumes.append(volume_name)

    return available_volumes

def exec_cmd(args):
    if sys.version_info >= (3, 0):
        rc = subprocess.run(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding='utf-8')
    else:
        rc = subprocess.Popen(args, stdout=subprocess.PIPE, \
                              stderr=subprocess.PIPE)
        rc.wait()

    if not rc.returncode:
        if sys.version_info >= (3, 0):
            if rc.stderr and not rc.stdout:
                result = rc.stderr.strip()
            else:
                result = rc.stdout.strip()
        else:
            stdout = rc.stdout.read()
            stderr = rc.stderr.read()
            if stderr and not stdout:
                result = stderr.strip()
            else:
                result = stdout.strip()

        try:
            return json.loads(result)
        except ValueError:
            if not result:
                result = 'success'
            return {'result': result}

    else:
        if sys.version_info >= (3, 0):
            raise Exception(rc.stderr.strip())
        else:
            stderr = rc.stderr.read()
            raise Exception(stderr.strip())


def export_volume_with_metadata(local_path, pool_name, volume_name, cluster_name = ''):
    if not cluster_name:
        export_cmd = 'rbd export --export-format=2 {pool}/{volume} {local_path} --cluster={cluster}' \
                     .format(pool = pool_name, volume = volume_name, local_path = local_path,
                             cluster = cluster_name)
    else:
        export_cmd = 'rbd export --export-format=2 {pool}/{volume} {local_path}' \
                     .format(pool = pool_name, volume = volume_name,
                             local_path = local_path)
    try:
        result = exec_cmd(export_cmd.split(' '))
    except Exception as e:
        print 'export volume with metadata failed, pool_name = {pool} volume = {volume}.' \
              .format(pool = pool_name, volume = volume_name) \
              + ' error msg = {err}'.format(err = e)
        return -1

    return 0


def import_volume_with_metadata(local_path, pool_name, volume_name, cluster_name = ''):
    if not cluster_name:
        import_cmd = 'rbd import --export-format=2 {local_path} {pool}/{volume} --cluster={cluster}' \
                     .format(local_path = local_path, pool = pool_name, volume = volume_name,
                             cluster = cluster_name)
    else:
        import_cmd = 'rbd import --export-format=2 {local_path} {pool}/{volume}' \
                     .format(local_path = local_path, pool = pool_name,
                             volume = volume_name)

    try:
        result = exec_cmd(import_cmd.split(' '))
        print result
    except Exception as e:
        print 'import volume with metadata failed, local_path = {local_path}.' \
              .format(local_path = local_path) \
              + ' error msg = {err}'.format(err = e)
        return -1

    return 0


def get_files_under_path(path):
    all_files = []
    for root_dir, dirs, files in os.walk(path):
        root_dir = root_dir if root_dir.endswith('/') else (root_dir + '/')
        for f in files:
            file_path = root_dir + f
            all_files.append(file_path)
    return all_files


def main():
    result = True
    opts, args = getopt.getopt(sys.argv[1:], 'a:e:i:', ['available=', 'export=', 'import='])
    if opts:
        for o, a in opts:
            # export only available volumes
            if o in ('-a', '--available'):
                available_volumes = get_available_volumes()
                for volume in available_volumes:
                    res = export_volume_with_metadata(a, 'volumes', volume)
                    if res:
                        result = False
                        print 'export available volume with metadata failed.'
            # export all volumes
            elif o in ('-e', '--export'):
                volumes = get_all_volumes()
                for volume in volumes:
                    res = export_volume_with_metadata(a, 'volumes', volume)
                    if res:
                        result = False
                        print 'export volume with metadata failed.'
            # import volumes from local path
            elif o in ('-i', '--import'):
                import_files = get_files_under_path(a)
                for import_file in import_files:
                    volume_name = import_file.split('/')[-1]
                    res = import_volume_with_metadata(import_file, 'volumes', volume_name)
#                    res = import_volume_with_metadata(import_file, 'rbd', volume_name)
                    if res:
                        result = False
                        print 'import volume with metadata failed.'

    else:
        print 'Get optional error!'
        return -1

    if not result:
        print 'Process failed.'
        return -1

    return 0


if __name__ == '__main__':
    main()
