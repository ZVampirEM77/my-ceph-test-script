# my-ceph-test-script

## migrate_volumes.py

### Usage

#### Export Available Volumes

```
$ python migrate_volumes.py -a $LOCAL_PATH
```

Export all available volumes from ceph 'volumes' pool to the specified
local path.

e.g.

```
$ python migrate_volumes.py -a /home/zvampirem
```

will export all available volumes from ceph 'volumes' pool to
the /home/zvampirem directory in local host.


#### Export All Volumes

```
$ python migrate_volumes.py -e $LOCAL_PATH
```

Export all volumes from ceph 'volumes' pool to the specified
local path


e.g.

```
$ python migrate_volumes.py -e /home/zvampirem
```

will export all volumes from ceph 'volumes' pool to the
/home/zvampirem directory in local host.


#### Import File to Ceph

```
$ python migrate_volumes.py -i $LOCAL_PATH
```

Import all files under the specified local path to ceph
'volumes' pool.


e.g.

```
$ python migrate_volumes.py -i /home/zvampirem
```

will import all files under /home/zvampirem directory to
ceph 'volumes' pool.
