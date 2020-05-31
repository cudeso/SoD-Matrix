#!/usr/bin/env python

from __future__ import print_function

""" machinetag2human.py
Copyright 2018 Aaron Kaplan <kaplan@cert.at>

Updated for SoD by Koen Van Impe <koen.vanimpe@cudeso.be>

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import sys
import json
# from datetime import datetime

if len(sys.argv) != 2:
    print("syntax: %s  <inputfile>" %(sys.argv[0],), file=sys.stderr)
    sys.exit(-1)

infile = sys.argv[1]

data = dict()
predicates = dict()


def print_header(data):
    print("""
# Segregation (or separation) of Duties (SoD) Matrix for CSIRTs, LEA and Judiciary (human readable version)

This is the Segregation (or separation) of Duties (SoD) Matrix for CSIRTs, LEA and Judiciary.

This SoD is also available as a [MISP taxonomy](https://github.com/MISP/misp-taxonomies).

See [An overview on enhancing technical cooperation between CSIRTs and LE](https://www.enisa.europa.eu/publications/support-the-fight-against-cybercrime-tools-for-enhancing-cooperation-between-csirts-and-le)

Version: %s
Generated from machine readable version. Please **DO NOT** edit this file directly in github, rather use the machinetag.json file.
| Phase                               | Cybercrime Fighting Activities      | CSIRT | LEA | Judge | Prosec | Training topcis |
|-----------------------------------  |-----------------------------------  | :---: | :---: | :---: | :---: |-----------|""" %(data['version']))                  # , str(datetime.now())))


def print_entries(data):
    for predicate in data['predicates']:
        predicates[predicate['value']] = predicate['expanded']

    for entry in data['values']:
        for t in entry['entry']:
            d = t.get('description', '')
            a = t.get('actors')
            actor_csirt = ""
            actor_lea = ""
            actor_judge = ""
            actor_prosec = ""
            for actor in a:
                if actor.lower() == "csirt":
                    actor_csirt = "x"
                if actor.lower() == "lea":
                    actor_lea = "x"
                if actor.lower() == "judge":
                    actor_judge = "x"
                if actor.lower() == "prosec":
                    actor_prosec = "x"
                    
            print('| %s | %s | %s | %s | %s  | %s | %s |' %(predicates[entry['predicate']], t['expanded'], actor_csirt, actor_lea, actor_judge, actor_prosec, d))


if __name__ == '__main__':
    try:
        with open(infile) as f:
            data = json.load(f)
            print_header(data)
            print_entries(data)
    except Exception as ex:
        print("could not open or parse json input file. Reason: %s" %str(ex))
        sys.exit(-2)