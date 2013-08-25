# Chef/Ansible template maker

This script takes a standard config file, and a set of regular expressions to
match configuration items, and generates a templated version of the same file
along with a companion attributes/default.rb file to drop into a cookbook. It
works best with configuration files that consist of large amounts of key/value
pairs, but will work with anything that you can match using regular
expressions.

## Pattern file

The logic of the program is in the parameters file. This file consists of
regular expression/action pairs. Each line in the config file is tested
against the regular expression, and the specified action is taken on the first
matching line.

Currently, the allowed actions are:

 * skip - prints the line unmodified - use this to match commented out lines
 * template - convert the line into a template. This action can take 'filters'
   as parameters, which will convert the key used in the vars file
   appropriately:
   * camel_to_underscore - the 'key' value should be converted from CamelCase
     to underscore_case in the attributes.rb.

For template actions, the pattern must contain two matching groups. The first
matching group identifies the key that will be used in the chef
attributes/default.rb (or ansible vars) file, and the second should surround
the value, which will be extracted and put in the attributes file.

## Examples

Templatize sshd_config:

    ./template_maker.py -p template_kv.txt -f test/sshd_config

The same, but for ansible:

    ./template_maker.py -p template_kv.txt -f test/sshd_config -t ansible

Running tests:

    python -m doctest [-v] template_maker.py
