def filter(s):
    """
    Converts CamelCase to underscore_case

    >>> filter("AnExample")
    'an_example'
    >>> filter("RSAAuthentication")
    'rsa_authentication'
    >>> filter("RhostsRSAAuthentication")
    'rhosts_rsa_authentication'
    >>> filter("X11Forwarding")
    'x11_forwarding'
    >>> filter("TestExampleABC")
    'test_example_abc'
    >>> filter("TestExampleA")
    'test_example_a'
    >>> filter("ATestExample")
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
