#Given a store name, this script generates a Checkout-compatible backup file.
#This script is handy for customers who want to script automated backups. 
#      python backup.py "My Store name" ~/testbackup.checkoutbackup
# Note that this script has no dependency on Checkout.app itself and therefore may be run from anywhere.

from argparse import ArgumentParser
import subprocess
import re
from tempfile import NamedTemporaryFile
import fileinput
import shutil
import sys
import os

parser = ArgumentParser(description='Standalone Checkout backup script.')
parser.add_argument('store',help='The store name to be backed up.')
parser.add_argument('destination',help='The backup destination file.')
args = parser.parse_args()

def check_output(*args,**kwargs): #new in python 2.7's subprocess...
    p = subprocess.Popen(*args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kwargs)
    output,errors = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode,errors)
    return output

#detect path to postgresql 8.3 if Checkout.app is installed in its usual location
if os.path.exists('/Applications/Checkout.app/'):
    os.environ['PATH'] = '/Applications/Checkout.app/Contents/Resources/postgres83/bin:' + os.environ['PATH']

#ensure we are using postgresql 8.3
for tool in ['psql','pg_dumpall','pg_dump']:
    try:
        version = check_output('{0} -V'.format(tool).split())
    except OSError as e:
        print e
        sys.stderr.write('Failed to find postgresql binaries in PATH\n' + os.environ['PATH'])
        sys.exit(-1)

    assert re.search('8\.3',version) is not None, "{0} is not from postgresql 8.3".format(tool)

#setup ~/.pgpass
pgpass_path = os.path.expanduser('~/.pgpass')
auth_line = 'localhost:5505:*:admin:admin\n'
if not os.path.exists(pgpass_path): #create pgpass
    with os.fdopen(os.open(pgpass_path,os.O_APPEND|os.O_CREAT|os.O_WRONLY,0600),'a') as pgpass:
        pgpass.write(auth_line)
else:
    with open(pgpass_path,'r') as pgpass:
        if not auth_line in pgpass.readlines():
            with open(pgpass_path,'a') as pgpass_a:
                pgpass_a.write(auth_line)

#determine store prefix from store name
#get the list of database prefixes
lines = check_output('psql -U admin -h localhost -p 5505 -l -t -A'.split())
db_prefix = None
for line in lines.split('\n')[0:-1]:
    matches = re.search('^(\w+)\|',line)
    if matches is None:
        continue
    prefix = matches.group(1)
    if prefix in ('postgres','template0','template1'):
        continue
    try:
        store_name = check_output('psql -U admin -h localhost -p 5505 {0} -t -A -c'.format(prefix).split() + ['SELECT checkout_name();']).rstrip()
    except subprocess.CalledProcessError:
        store_name = None
    if store_name == args.store:
        db_prefix = prefix
        break

assert db_prefix is not None, 'Store "{0}" not found.'.format(args.store)
    
#now we have the store, so emulate the Checkout backup procedure
userdump = check_output('pg_dumpall -g -U admin -p 5505 -h localhost'.split()).decode('utf-8')
user_section = ''
#substitute and filter the users section
for line in userdump.split('\n'):
    for item in [db_prefix, u'SET ', u'--', u'\connect']:
        if item in line:
            user_section += re.sub(u'{0}|postgres'.format(db_prefix),u'*DATABASE_NAME*',line) + u'\n'

tmp_backup_file = NamedTemporaryFile(delete=False)
tmp_backup_file.write(user_section.encode('utf-8'))
tmp_backup_file.flush()

#dump the database
#print 'pg_dump -h localhost -p 5505 -E UTF-8 -U admin {0} >> {1}'.format(db_prefix,tmp_backup_file.name)

proc = subprocess.Popen('pg_dump -h localhost -p 5505 -E UTF-8 -U admin {0}'.format(db_prefix).split(),stdout=tmp_backup_file)
proc.wait()
assert proc.returncode == 0,'pg_dump failed'

#replace the changing prefix with the placeholder
for line in fileinput.input([tmp_backup_file.name],inplace=1):
    line = line.decode('utf-8')
    line = re.sub(u'\t{0}'.format(db_prefix),u'\t*DATABASE_NAME*',line)
    line = re.sub(u'"{0}'.format(db_prefix),u'"*DATABASE_NAME*',line)
    print line.encode('utf-8'),

#compress the backup
subprocess.check_call('gzip --best {0}'.format(tmp_backup_file.name).split())

#move the backup to the destination
shutil.move('{0}.gz'.format(tmp_backup_file.name),args.destination)





