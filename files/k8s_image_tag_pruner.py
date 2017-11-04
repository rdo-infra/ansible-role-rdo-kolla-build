#!/usr/bin/env python
#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import sys
import json
from datetime import datetime

# Given a list of image stream tags ("oc get istag -o json"), returns a list
# of images older than MAX_AGE

# Seven days
MAX_AGE = 86400 * 7
NOW = datetime.utcnow()
# These tags should never be deleted
WHITELIST = [
    'tripleo-ci-testing',
    'current-tripleo',
    'current-tripleo-rdo'
]
DEBUG = False


def usage():
    print("Usage: oc get imagestreams -o json | tag_pruner.py")

try:
    imagestreams = json.load(sys.stdin)
except ValueError:
    print("The data provided doesn't seem to be valid JSON")
    usage()


for imagestream in imagestreams['items']:
    name, tag = imagestream['metadata']['name'].split(':')
    timestamp = imagestream['metadata']['creationTimestamp']
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    delta = NOW - timestamp
    if delta.total_seconds() > MAX_AGE and tag not in WHITELIST:
        if DEBUG:
            print("%s:%s | %s" % (name, tag, delta))
        else:
            print("%s:%s" % (name, tag))
