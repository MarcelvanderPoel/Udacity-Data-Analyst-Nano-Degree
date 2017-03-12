#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import Counter
import csv

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
#both name and operator have next to a standard description a variety of international descriptions
intdescriptions = re.compile(r'name:|operator:')

KEY_SET = set()
POSTCODE_SET=set()
WRONG_POSTAL_CODE_LIST=[]
KEY_COUNT_LIST = []
SELECTED_TAGS = ('node', 'way', 'relation')

DATADIR = ""
DATAFILE = "Postalcode.csv"
ADDRESS_DICT = {}

def parse_file(datafile):
    address_dict={}

    with open(datafile, 'rb') as f:
        # read scraped postal code information from csv file into a dictionary
        r = csv.reader(f, delimiter='|')
        count = 0
        for line in r:
            if count == 0:
                pass
            else:
                street_city_list = []
                street_city_list.append(line[1])
                street_city_list.append(line[2])
                address_dict[line[0]] = street_city_list
            count += 1

    return address_dict

def shape_element(element):

    if element.tag in SELECTED_TAGS:
    # only select node, way and relation. Skip the top level osm tag
        json_object = {}
        # type of object (node, way or relation) and visibility are stored
        json_object['toptype'] = element.tag
        if 'visible' in element.attrib:
            json_object['visible'] = element.attrib['visible']
        else:
            json_object['visible'] = 'true'

        # all elements have the following attributes: changeset, id, timestamp, uid, user, version.
        json_object['id'] = element.attrib['id']
        # version information is stored in a subobject 'created'
        created = {}
        created['changeset'] = element.attrib['changeset']
        created['timestamp'] = element.attrib['timestamp']
        created['uid'] = element.attrib['uid']
        created['user'] = element.attrib['user']
        created['version'] = element.attrib['version']
        json_object['created'] = created

        # the node element has two additional attributes: lat and lon that are stored in a 'pos' array
        if 'lat' in element.attrib:
            pos = [float(element.attrib['lat']), float(element.attrib['lon'])]
            json_object['pos'] = pos

        address = {}
        railway = {}
        ref={}
        noderefs = []

        for child in element:
            # the node, way and relation element can have tag elements with key/value pairs
            # the way element has 2 or more nd elements with a ref attribute
            # the relation element has n member elements with a ref, role and type attribute
            if child.tag=='tag':
                # <tag> contains a key/value pair
                cakey=child.attrib['k']
                cavalue=child.attrib['v']

                # Resolve situations with 2 columns
                cakey=cakey.replace(':exact','')
                cakey=cakey.replace(':bridge','')
                if cakey.count(':') == 2:
                    li = cakey.rsplit(':', 1)
                    cakey=li[0]+li[1]

                KEY_SET.add(cakey)
                KEY_COUNT_LIST.append(cakey)

                if not (problemchars.match(cakey)) and (cakey.count(':') < 2) and not (intdescriptions.match(cakey)):
                    if cakey.count(':') == 1:
                        # There is 1 column in the key, if appropriate, make a list based on part before column
                        attrib_list = cakey.split(':')
                        if attrib_list[0] == 'addr':
                            # some postalcodes have structure '9999 XX' instead of '9999XX'

                            if attrib_list[1]=='postcode':
                                address[attrib_list[1]] = cavalue.replace(" ", "")
                                POSTCODE_SET.add(cavalue.replace(" ", ""))
                            else:
                                address[attrib_list[1]] = cavalue
                        elif attrib_list[0] == 'railway':
                            railway[attrib_list[1]] = cavalue
                        elif attrib_list[0] == 'ref':
                            ref[attrib_list[1]] = cavalue
                        else:
                            tagje = cakey.replace(':', '_')
                            json_object[tagje] = cavalue
                    else:
                        # There is no column in the key
                        json_object[cakey] = cavalue
                else:
                    print '### Wrongly Formated ### ', cakey, ' : ', cavalue
            elif child.tag=='nd':
                noderefs.append(child.attrib['ref'])
            else: #child.tag=='member'
                # a <member> contains a dictionary
                for key in child.attrib:
                    # iterate over the dictionary
                    json_object[key] = child.attrib[key]
        # Store all built lists
        if noderefs:
            json_object['node_refs'] = noderefs
        if address:

            if 'postcode' in address:
                if 'city' in address:
                    if not str(address['city'])==str(ADDRESS_DICT[address['postcode']][1]):
                        print 'oud ', address['city']
                        print 'nwe ', ADDRESS_DICT[address['postcode']][1]
                if 'street' in address:
                    if (not address['street'] == ADDRESS_DICT[address['postcode']][0]) and (not address['postcode'] in ['4191KX','4116ET','4191XT']):
                        WRONG_POSTAL_CODE_LIST.append( [address['postcode'], address['street'], address['housenumber'], address['city'], ADDRESS_DICT[address['postcode']][0], ADDRESS_DICT[address['postcode']][1]] )

            json_object['address'] = address
        if railway:
            json_object['railway'] = railway
        if ref:
            json_object['reference'] = ref

        return json_object
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

if __name__ == "__main__":

    ADDRESS_DICT = parse_file(DATAFILE)

    process_map('GeldermalsenNetherlands.osm', False)

    pprint = pprint.PrettyPrinter(width=180)

    # Change False to True to print analytic data about the data set

    # all used tags in alphabetical order to discover groups based on ':'.
    if False:
        pprint.pprint(KEY_SET)

    # list of used tags sorted on the number of times used (relevance)
    if False:
        pprint.pprint(Counter(KEY_COUNT_LIST))

    # list of all different postal codes used for addresses as input for ScrapePostalCodeInformation.py
    if False:
        pprint.pprint(POSTCODE_SET)

    #print postalcode, OSM street, OSM housenumber, OSM city, postcode.nl street, postcode.nl city
    if False:
        WRONG_POSTAL_CODE_LIST.sort()
        pprint.pprint(WRONG_POSTAL_CODE_LIST)

    #print the number of addresses where postalcode and address do not match
    if False:
        print 'Number of adresses with wrong postalcode: ', len(WRONG_POSTAL_CODE_LIST)


