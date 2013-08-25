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
    elif args.templatetype == 'ansible':
        template_pattern = '{{ %s_%s }}'

    # Options in this case are various filters you can use on the key name
    key = match.group(1)
    for o in options:
        filterfunc = getattr(filters, o, None)
        if filterfunc:
            key = filterfunc(key)
        else:
            print "ERROR: unknown filter: %s" % o
            sys.exit(1)
    attrs.append((key, match.group(2)))
    return line[:match.start(2)] + template_pattern % (
        args.attrprefix, key) + line[match.end(2):]
