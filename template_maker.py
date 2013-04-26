#!/usr/bin/env python
# Script to automatically templatize a config file for chef
# TODO
#   - getopts
#   - output both converted and attrs files (with default names)
#       input_file.erb and attrs_default.rb
#   - customizable attr_prefix

# Pattern file format
# /regex/ action
#
# Actions:
#   skip - don't transform the line (useful for comments)
#   template - transform the line - matching group 2 is the value, matching
#       group
#   1 is the name
import re
import sys
import argparse

parser = argparse.ArgumentParser(
        description='Automatic chef template generator.')
parser.add_argument('-p', '--patfile', required=True,
        help='File containing pattern/action pairs')
parser.add_argument('-f', '--file', required=True,
        help='File to convert to a template')
parser.add_argument('-o', '--output',
        help='File to output the template to')
parser.add_argument('-a', '--attrs', default='default.rb',
        help='File to output the chef attribute definitions to')
parser.add_argument('-ap', '--attrprefix', default='foo',
        help='Prefix to add to attribute default definitions')
args = parser.parse_args()

# Add some dynamic defaults
if args.output is None:
    args.output = "%s.erb" % args.file

def camel_to_underscore(s):
    new_s = []
    for i, c in enumerate(s):
        next_is_upper = i < len(s) - 1 and s[i+1].isupper()
        if c.isupper() and not next_is_upper and i != 0:
            new_s.append('_')
        new_s.append(c.lower())
    return ''.join(new_s)

pat_fh = open(args.patfile)
patterns = []
for line in pat_fh:
    line = line.strip()
    if line[0] == '#':
        continue
    parts = line.split()
    parts[0] = parts[0].strip('/')
    patterns.append(parts)
    print parts
pat_fh.close()

attrs = [] # For the attributes/default.rb file
fh = open(args.file)
ofh = open(args.output, "w")
for line in fh:
    for p in patterns:
        m = re.search(p[0], line)
        if m:
            action = p[1]
            if action == 'skip':
                # Don't transform the line
                pass
            elif action == 'template':
                line = line[:m.start(2)] + '<%%= node[:%s][:%s] %%>' % (
                        args.attrprefix, m.group(1)) + line[m.end(2):]
                attrs.append((m.group(1), m.group(2)))
            elif action == 'camel_template':
                # TODO - merge this and the template option
                line = line[:m.start(2)] + '<%%= node[:%s][:%s] %%>' % (
                        args.attrprefix, camel_to_underscore(m.group(1))) + \
                        line[m.end(2):]
                attrs.append((camel_to_underscore(m.group(1)), m.group(2)))
            else:
                print "ERROR: unknown action: %s" % p[1]
                sys.exit(1)
            break
    ofh.write(line)
fh.close()
ofh.close()

afh = open(args.attrs, "w")
for k, v in attrs:
    afh.write("default[:%s][:%s] = '%s'\n" % (args.attrprefix, k, v))
afh.close()
