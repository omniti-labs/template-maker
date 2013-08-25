"""
Contains the various transformation functions used for template lines
"""
import sys

import filters


def action_skip(line, attrs, match, args, options):
    """Don't transform the line in any way"""
    return line


def action_delete(line, attrs, match, args, options):
    """Delete the line from the template"""
    return None


def action_template(line, attrs, match, args, options):
    template_pattern = "$%s%s"  # Stupid default that shouldn't ever be used
    if args.templatetype == 'chef':
        template_pattern = '<%%= node[:%s][:%s] %%>'
        key_separator = '][:'
    elif args.templatetype == 'ansible':
        template_pattern = '{{ %s_%s }}'
        key_separator = '_'

    # Options in this case are various filters you can use on the key name
    keys = match.groups()[:-1]
    for o in options:
        filterfunc = getattr(filters, o, None)
        if filterfunc:
            newkeys = []
            for k in keys:
                newkeys.append(filterfunc(k))
            keys = newkeys
        else:
            print "ERROR: unknown filter: %s" % o
            sys.exit(1)
    last_match = len(match.groups())
    attrs.append((keys, match.group(last_match)))
    return line[:match.start(last_match)] + template_pattern % (
        args.attrprefix, key_separator.join(keys)) + line[
            match.end(last_match):]
