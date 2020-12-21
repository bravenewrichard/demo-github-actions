import os
import re
from shutil import copyfile
from sys import exit


import semver
import requests
from requests.exceptions import HTTPError

""" STEPS
1. check all stack info for latest XCode version
2. compare latest with cached version
3. if greater, continue...
4. bitrise update
5. modify bitrise.yml (update stack value)
6. bitrise run primary
"""


PREV_XCODE_VER = os.environ.get('PREV_XCODE_VER', '0.0.0')

ALL_STACK_INFO = 'https://app.bitrise.io/app/6c06d3a40422d10f/all_stack_info'
pattern = 'osx-xcode-'
INFILE = 'bitrise.yml'
OUTFILE = 'out.yml'
SEMVER_PREV = 'SEMVER_PREV'

"""
 jq ' . | keys'
[
  "available_stacks",
  "project_types_with_default_stacks",
  "running_builds_on_private_cloud"
]
"""

resp = requests.get(ALL_STACK_INFO)
resp.raise_for_status()
resp_json = resp.json()


def parse_semver(raw_str):
    parsed = raw_str.split(pattern)[1]
    if parsed[-1] == 'x':
        p = parsed.split('.x')[0]
        return '{0}.0'.format(p)
    else:
        return False


def largest_version(resp):
    count = 0
    for item in resp:
        print(item)
        if pattern in item:
            p = parse_semver(item)
            if p:
                if count == 0 or semver.compare(largest, p) == -1:
                    largest = p 
                count += 1
    return '{0}.x'.format(largest.split('.0')[0])
    #return largest


def write_semver(new_semver):

    try:
        copyfile(INFILE, OUTFILE)
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    with open(OUTFILE, 'r+') as f:
        text = f.read()
        text = re.sub('{XCODE_VERSION}', new_semver, text)
        f.seek(0)
        f.write(text)
        f.truncate()

def semver_prev():
    with open(SEMVER_PREV, 'r') as f:
        val = f.read()
        return val 


def semver_prev_write(new_semver):
    with open(SEMVER_PREV, 'w+') as f:
        f.write(new_semver)
        f.truncate()
    
try:
    resp = requests.get(ALL_STACK_INFO)
    resp.raise_for_status()
    resp_json = resp.json()
    r = resp_json['available_stacks']
except HTTPError as http_error:
    print('An HTTP error has occurred: {http_error}')

except Exception as err:
    print('An exception has occurred: {err}')

largest_semver = largest_version(r)
write_semver(largest_semver)
write_semver('9.3.8')
print('PREV_XCODE_VER: {0}'.format(PREV_XCODE_VER))
os.environ['PREV_XCODE_VER'] = largest_semver

previous_semver = semver_prev()
if previous_semver:
    print('the prev semver is: {0}'.format(previous_semver))
else:
    semver_prev_write(largest_semver)


