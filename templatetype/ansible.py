"""
Ansible template output module
"""


class TemplateType(object):
    def __init__(self, args):
        # Output template file extension
        self.template_extension = 'j2'
        # Default vars/attrs file name
        self.attrs_file = 'main.yml'
        # Key prefix
        self.prefix = args.attrprefix

    def write_attrs(self, fh, attrs):
        "Writes the attributes file out"
        fh.write("---\n")
        for k, v in attrs.items():
            # Yaml interprets some values as booleans, and they don't get put
            # correctly into the template, so force them to be strings in that
            # case.
            if v in ['Y', 'yes', 'true', 'Yes']:
                v = '"yes"'
            if v in ['N', 'no', 'false', 'No']:
                v = '"no"'
            fh.write("%s_%s: %s\n" % (self.prefix, '_'.join(k), v))

    def regular_template_line(self, line_start, line_end, keys):
        return line_start + '{{ %s_%s }}' % (
            self.prefix, '_'.join(keys)) + line_end

    def loop_template_line(self, line_start, keys):
        """Generate a loop in the template given a list of values"""
        return (
            '{%% for i in %s_%s %%}' % (self.prefix, '_'.join(keys)),
            '%s{{ i }}' % line_start,
            '{% endfor %}'
        )
