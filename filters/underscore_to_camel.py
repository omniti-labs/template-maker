import re

def filter(s):
    """
    Converts underscore_case to CamelCase

    >>> filter("an_example")
    'AnExample'
    >>> filter("rsa_authentication")
    'RsaAuthentication'
    >>> filter("rhosts_rsa_authentication")
    'RhostsRsaAuthentication'
    >>> filter("x11_forwarding")
    'X11Forwarding'
    >>> filter("test_example_a")
    'TestExampleA'
    >>> filter("a_test_example")
    'ATestExample'
    >>> filter("another_example_")
    'AnotherExample'
    """
    s = s[0].upper() + s[1:]
    def underscore_repl(m):
        return m.group(1).upper()
    return re.sub('_(.?)', underscore_repl, s)
