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


def camel_to_underscore(s):
    """
    Converts CamelCase to underscore_case

    >>> camel_to_underscore("AnExample")
    'an_example'
    >>> camel_to_underscore("RSAAuthentication")
    'rsa_authentication'
    >>> camel_to_underscore("RhostsRSAAuthentication")
    'rhosts_rsa_authentication'
    >>> camel_to_underscore("X11Forwarding")
    'x11_forwarding'
    >>> camel_to_underscore("TestExampleABC")
    'test_example_abc'
    >>> camel_to_underscore("TestExampleA")
    'test_example_a'
    >>> camel_to_underscore("ATestExample")
    'a_test_example'
    """
    new_s = []
    for i, c in enumerate(s):
        next_is_upper = i < len(s) - 1 and s[i+1].isupper()
        prev_is_upper = i > 0 and s[i-1].isupper()
        if i > 0:  # Never include an underscore at the beginning
            if c.isupper() and not next_is_upper and i < len(s) - 1:
                new_s.append('_')
            elif c.isupper() and not prev_is_upper:
                new_s.append('_')
        new_s.append(c.lower())
    return ''.join(new_s)


def process_template_line(line, attrs, match, func=None):
    template_pattern = "$%s%s"  # Stupid default that shouldn't ever be used
    if args.templatetype == 'chef':
        template_pattern = '<%%= node[:%s][:%s] %%>'
    elif args.templatetype == 'ansible':
        template_pattern = '{{ %s_%s }}'

    if func is None:
        func = lambda x: x
    attrs.append((func(match.group(1)), match.group(2)))
    return line[:match.start(2)] + template_pattern % (
        args.attrprefix, func(match.group(1))) + line[match.end(2):]


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
        if line[0] == '#':
            continue
        parts = line.split()
        parts[0] = parts[0].strip('/')
        patterns.append(parts)
    pat_fh.close()

    # Now generate the template file
    attrs = []  # For the attributes/default.rb file
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
                    line = process_template_line(line, attrs, m)
                elif action == 'camel_template':
                    line = process_template_line(line, attrs, m,
                                                 camel_to_underscore)
                else:
                    print "ERROR: unknown action: %s" % p[1]
                    sys.exit(1)
                break
        ofh.write(line)
    fh.close()
    ofh.close()

    # Now write out the defaults file
    afh = open(args.attrs, "w")

    # Stupid default that shouldn't ever be used
    defaults_pattern = "%s%s = %s\n"
    defaults_prefix = ''
    if args.templatetype == 'chef':
        defaults_pattern = "default[:%s][:%s] = '%s'\n"
    elif args.templatetype == 'ansible':
        defaults_prefix = '---\n'
        defaults_pattern = '%s_%s: %s\n'
    afh.write(defaults_prefix)
    for k, v in attrs:
        afh.write(defaults_pattern % (args.attrprefix, k, v))
    afh.close()
