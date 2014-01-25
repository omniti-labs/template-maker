"""
Chef template output module
"""


class TemplateType(object):
    def __init__(self, args):
        # Output template file extension
        self.template_extension = 'erb'
        # Output vars/atts file name
        self.attrs_file = 'default.rb'

        self.prefix = args.attrprefix

    def write_attrs(self, fh, attrs):
        "Writes the attributes file out"
        for k, v in attrs.items():
            if isinstance(v, basestring):
                v = "'%s'" % v
            fh.write("default[:%s][:%s] = %s\n" % (
                self.prefix, '][:'.join(k), v))

    def regular_template_line(self, line_start, line_end, keys):
        return line_start + '<%%= node[:%s][:%s] %%>' % (
            self.prefix, '][:'.join(keys)) + line_end

    def loop_template_line(self, line_start, keys):
        """Generate a loop in the template given a list of values"""
        return (
            '<%% node[:%s][:%s].each do |i| %%>' % (
                self.prefix, '][:'.join(keys)),
            '%s<%%= i %%>' % line_start,
            '<% end %>'
        )
