#!/usr/bin/env python
# Referenced from https://productize.be/kicad-bom-generation/
# This script needs some improvement
# (c) 2015 Productize <joost@productize.be>

import sys
import copy
import collections

from bs4 import BeautifulSoup


def stringify(obj):
    if type(obj) is list:
        item_str = ';'.join(c['Reference'])
    else:
        item_str = str(obj)
    return '"{}"'.format(item_str)


soup = BeautifulSoup(open(sys.argv[1]), 'lxml')

date = soup.design.date.contents[0]

components = []

standard_fields = ['Reference',
                   'Value',
                   'Quantity',
                   'Supplier',
                   'Supplier Part Number',
                   'Manufacturer',
                   'Manufacturer Part Number']

extra_fields = []

for c in soup.components.find_all("comp"):
    new_components = {}
    new_components['Reference'] = [c['ref']]
    new_components['Value'] = c.value.contents[0]
    new_components['Quantity'] = 1
    new_components['Identifier'] = ''
    new_components['Package'] = ''
    new_components['Supplier'] = ''
    new_components['Supplier Part Number'] = ''
    new_components['Manufacturer'] = ''
    new_components['Manufacturer Part Number'] = ''
    for f in c.find_all("field"):
        new_components[f['name']] = f.contents[0]
        if f['name'] not in standard_fields:
            if f['name'] not in extra_fields:
                extra_fields.append(f['name'])
    found = None
    new_comp_no_ref = {}
    for k in new_components.keys():
        if k not in ['Reference', 'Quantity']:
            new_comp_no_ref[k] = new_components[k]
    for c2 in components:
        c2_no_ref = {}
        for k in c2.keys():
            if k not in ['Reference', 'Quantity']:
                c2_no_ref[k] = c2[k]
        print str(c2_no_ref)
        print str(new_comp_no_ref)
        if str(c2_no_ref) == str(new_comp_no_ref):
            found = c2
            c2['Reference'].append(c['ref'])
            c2['Quantity'] += 1
            break
    if found is None:
        components.append(new_components)



with open(sys.argv[2], "w") as f:
    title_str = ','.join(standard_fields)
    f.write(title_str + '\r\n')
    for c in components:
        l = [stringify(c[field]) for field in standard_fields]
        f.write(','.join(l))
        f.write('\r\n')
