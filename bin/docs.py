#!/usr/bin/env python

from __future__ import unicode_literals

import os
import sys
import logging
import datetime
import json
import io

if __name__ == '__main__':

    whoami = sys.argv[0]
    whoami = os.path.abspath(whoami)

    bin = os.path.dirname(whoami)
    root = os.path.dirname(bin)

    sources = os.path.join(root, 'sources')
    data = os.path.join(root, 'data')

    latest = os.path.join(data, "sources-spec-latest.json")
    readme = os.path.join(sources, "README.md")

    fh = io.open(latest, "r")
    spec = json.load(fh)

    lookup = {}

    for id, details in spec.items():
        lookup[details['name']] = id

    names = lookup.keys()
    names.sort()

    now = datetime.datetime.now()
    ymd = now.strftime("%Y-%m-%d")

    docs = io.open(readme, "w")
    docs.write("# sources\n\n")

    docs.write("_This file was generated by the `bin/docs.py` script on %s_\n\n" % ymd)

    docs.write("_All sources listed below are currently used to populate Who's On First records or will be added to Who's On First records in the near future._")

    for n in names:

        id = lookup[n]
        details = spec[id]

        docs.write("## %s\n\n" % (details['fullname']))

        if details.get('description'):
            docs.write("_%s_ \n\n" % (details['description']))

        if details.get('edtf:deprecated'):
            if not details['edtf:deprecated'] == 'uuuu':
                docs.write("* %s %s.\n" % ('This source was deprecated on', details['edtf:deprecated']))

        for k in ('id', 'name', 'prefix'):

            if details[k] == '':
                continue
            docs.write("* %s: `%s`\n" % (k, details[k]))

        if details.get('license_type'):
            docs.write("* %s: _%s_\n" % ('license_type', details['license_type']))

        if details.get('license_text'):
            docs.write("* %s: _%s_\n" % ('license_text', details['license_text']))

        if not details.get('url') == "":
            docs.write("* %s: _%s_\n" % ('url', details['url']))

        if details.get('remarks'):
            docs.write("* %s: _%s_\n" % ('remarks', details['remarks']))

        if details.get('license') and details.get('license').startswith("http"):
            docs.write("* %s: _%s_\n" % ('license', details['license']))
        else:
            docs.write("* %s: `%s`\n" % ('license', details['license']))

        if details.get('src:via'):
            docs.write("\n  This source includes `CC-BY compatible` data from the following organizations:\n")
            for via in details['src:via']:
                if via['source_note']:
                    docs.write("  \t* **%s**: [%s](%s) - %s\n" % (via["context"],via["source_name"],via["source_link"],via["source_note"]))
                else:
                    docs.write("  \t* **%s**: [%s](%s)\n" % (via["context"],via["source_name"],via["source_link"]))

        usage = []
        
        if details.get('usage_concordance'):
            if details['usage_concordance'] == 1:
                usage.append("`concordance`")
                
        if details.get('usage_property'):        
            if details['usage_property'] == 1:
                usage.append("`property`")

        if details.get('usage_geometry'):
            if details['usage_geometry'] == 1:
                usage.append("`geometry`")

        all_uses = ', '.join(usage)

        if not usage == []:
            docs.write("* %s: %s\n" % ('usage', all_uses))

        docs.write("\n")

    docs.close()