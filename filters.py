"""
Filters that can be applied to various parts of the template keys
"""


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
