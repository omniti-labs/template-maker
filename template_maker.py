#!/usr/bin/env python
# Script to automatically templatize a config file for chef

# Pattern file format
# /regex/ action
#
# Actions:
#   skip - don't transform the line (useful for comments)
#   template - transform the line - matching group 2 is the value, matching
#       group
#   1 is the name
import os
import re
import sys
import argparse
from collections import OrderedDict

import actions


def parse_args():
    parser = argparse.ArgumentParser(
        description='Automatic erb/jinja2 template generator.')
    parser.add_argument(
        '-p', '--patfile', required=True,
        help='File containing pattern/action pairs')
    parser.add_argument(
        '-t', '--templatetype', default='chef',
        choices=['chef', 'ansible'],
        help='Type of template to generate')
    parser.add_argument(
        '-f', '--file', required=True, help='File to convert to a template')
    parser.add_argument(
        '-o', '--output', help='File to output the template to')
    parser.add_argument(
        '-a', '--attrs',
        help='File to output the default variable settings to')
    parser.add_argument(
        '-ap', '--attrprefix', default='foo',
        help='Prefix to add to attribute default definitions')
    args = parser.parse_args()
    # Add some dynamic defaults
    if args.output is None:
        ext = ''
        if args.templatetype == 'chef':
            ext = 'erb'
        elif args.templatetype == 'ansible':
            ext = 'j2'
        args.output = "%s.%s" % (args.file, ext)
    if args.attrs is None:
        args.attrs = 'defaults'
        if args.templatetype == 'chef':
            args.attrs = 'default.rb'
        elif args.templatetype == 'ansible':
            args.attrs = 'vars.yml'
        args.attrs = os.path.join(os.path.dirname(args.output), args.attrs)
    return args

if __name__ == '__main__':
    args = parse_args()

    # Parse the pattern file
    pat_fh = open(args.patfile)
    patterns = []
    for line in pat_fh:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        parts = line.split()
        parts[0] = parts[0].strip('/')
        patterns.append(parts)
    pat_fh.close()

    # Now generate the template file
    attrs = OrderedDict()  # For the attributes/default.rb file
    fh = open(args.file)

    out_lines = []
    for line in fh:
        for p in patterns:
            m = re.search(p[0], line)
            if m:
                action = p[1]
                actionfunc = getattr(actions, "action_" + action, None)
                if actionfunc:
                    actionfunc(line, out_lines, attrs, m, args, p[2:])
                else:
                    print "ERROR: unknown action: %s" % p[1]
                    sys.exit(1)
                break
        else:
            # No match, copy as is
            out_lines.append({'action': 'default', 'text': line})
    fh.close()

    ofh = open(args.output, "w")
    for line in out_lines:
        ofh.write(line['text'])
    ofh.close()

    # Now write out the defaults file
    afh = open(args.attrs, "w")

    # Stupid default that shouldn't ever be used
    defaults_pattern = "%s%s = %s\n"
    defaults_prefix = ''
    defaults_key_separator = '_'
    if args.templatetype == 'chef':
        defaults_pattern = "default[:%s][:%s] = '%s'\n"
        defaults_key_separator = "][:"
    elif args.templatetype == 'ansible':
        defaults_prefix = '---\n'
        defaults_pattern = '%s_%s: %s\n'
    afh.write(defaults_prefix)
    for k, v in attrs.items():
        afh.write(defaults_pattern % (args.attrprefix,
                                      defaults_key_separator.join(k), v))
    afh.close()
