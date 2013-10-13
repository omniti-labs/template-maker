"""
Contains the various transformation functions used for template lines
"""
import sys

import filters


def action_skip(line, out_lines, attrs, match, tmod, options):
    """Don't transform the line in any way"""
    out_lines.append({'action': 'skip', 'text': line})


def action_delete(line, out_lines, attrs, match, tmod, options):
    """Delete the line from the template"""
    pass


def action_template(line, out_lines, attrs, match, tmod, options):
    # Options in this case are various filters you can use on the key name
    keys = match.groups()[:-1]
    for o in options:
        try:
            # Get the module for the filter, automatically importing it on
            # demand if it isn't already.
            mod = getattr(
                filters, o,
                __import__('filters.%s' % o, globals(), locals()))
        except ImportError:
            # The automatic import failed
            print "ERROR: unknown filter: %s" % o
            sys.exit(1)
        newkeys = []
        for k in keys:
            # Filter modules have a single function called 'filter'
            newkeys.append(mod.filter(k))
        keys = newkeys
    last_match = len(match.groups())
    keys = tuple(keys)  # Make keys hashable (usable as a dict key)
    new_line_start = line[:match.start(last_match)]
    if keys in attrs:
        # We have a duplicate key, time to deal with it
        last_line = out_lines[-1]
        if last_line['action'] == 'template' and last_line['attr'] == keys:
            # Great, we just processed a key line, which means we can do this
            # set of keys as a sequence.
            del(out_lines[-1])
            loop_lines = tmod.loop_template_line(new_line_start, keys)
            for l in loop_lines:
                out_lines.append({'action': 'template_loop', 'attr': keys,
                                  'text': '%s\n' % l})
            attrs[tuple(keys)] = [attrs[tuple(keys)], match.group(last_match)]
        elif last_line['action'] == 'template_loop' and \
                last_line['attr'] == keys:
            # We don't need to print anything to out_lines, we just need to
            # append the items to the list
            attrs[tuple(keys)].append(match.group(last_match))
        else:
            print "ERROR: non-consecutive duplicate key '%s'" % ','.join(keys)
            sys.exit(1)
    else:
        # Normal, regular key, we're ok
        attrs[tuple(keys)] = match.group(last_match)
        new_line = tmod.regular_template_line(
            new_line_start, line[match.end(last_match):], keys)
        out_lines.append({'action': 'template', 'attr': keys,
                          'text': new_line})
