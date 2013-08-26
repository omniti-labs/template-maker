"""
Chef template output module
"""

# Output template file extension
template_extension = 'erb'

# Output vars/atts file name
attrs_file = 'default.rb'


def write_attrs(fh, attrs, prefix):
    "Writes the attributes file out"
    for k, v in attrs.items():
        fh.write("default[:%s][:%s] = '%s'\n" % (prefix, '][:'.join(k), v))


def regular_template_line(line_start, line_end, prefix, keys):
    return line_start + '<%%= node[:%s][:%s] %%>' % (
        prefix, '][:'.join(keys)) + line_end


def loop_template_line(line_start, prefix, keys):
    """Generate a loop in the template given a list of values"""
    return (
        '<%% node[:%s][:%s].each do |i| %%>' % (prefix, '][:'.join(keys)),
        '%s<%%= i %%>' % line_start,
        '<% end %>'
    )
