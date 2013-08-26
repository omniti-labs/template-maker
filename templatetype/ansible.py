"""
Ansible template output module
"""

# Output template file extension
template_extension = 'j2'

# Output vars/atts file name
attrs_file = 'vars.yml'


def write_attrs(fh, attrs, prefix):
    "Writes the attributes file out"
    fh.write("---\n")
    for k, v in attrs.items():
        fh.write("%s_%s: %s\n" % (prefix, '_'.join(k), v))


def regular_template_line(line_start, line_end, prefix, keys):
    return line_start + '{{ %s_%s }}' % (prefix, '_'.join(keys)) + line_end


def loop_template_line(line_start, prefix, keys):
    """Generate a loop in the template given a list of values"""
    return (
        '{%% for i in %s_%s %%}' % (prefix, '_'.join(keys)),
        '%s{{ i }}' % line_start,
        '{% endfor %}'
    )
