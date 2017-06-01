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

# Filters a list of OpenShift registry images from a json format based on
# a tag
# Usage: oc get imagestreams -o json | tag_filter.py <tag>

# The alternative being:
# oc get is -o template --template='{{ range .items }}{{$name:=.metadata.name}}{{ range .status.tags }}{{ if eq .tag "source_tag" }}{{ $name }}{{ "\n" }}{{ end }}{{ end }}{{ end -}}' # noqa
# Or in an Ansible command:
# oc get is -o template --template='{% raw %}{{ range .items }}{{$name:=.metadata.name}}{{ range .status.tags }}{{ if eq .tag {% endraw %}"{{ source_tag }}"{% raw %} }}{{ $name }}{{ "\n" }}{{ end }}{{ end }}{{ end -}}{% endraw %}' # noqa


def usage():
    print("Usage: oc get imagestreams -o json | tag_filter.py <tag>")

try:
    source_tag = sys.argv[1]
except IndexError:
    print('No tag filter provided')
    usage()

try:
    images = json.load(sys.stdin)
except ValueError:
    print("The data provided doesn't seem to be valid JSON")
    usage()

for image in images['items']:
    for tag in image['status']['tags']:
        if source_tag == tag['tag']:
            print(image['metadata']['name'])
            break
