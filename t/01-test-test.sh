#!/bin/bash

# Load testing framework
. ./testlib.sh

TEST_SUITE_NAME="Test the testing framework"

# Number of tests
TOTAL_TESTS=9

assert 'true' 'true'
assert 'inverse' '! false'
assert '[[ condition ]]' '[[ -n "FOO" ]]'

SOME_VAR=foo
BLANK_VAR=
assert '[[ -n $SOME_VAR ]]' '[[ -n $SOME_VAR ]]'
assert '[[ -z $BLANK_VAR ]]' '[[ -z $BLANK_VAR ]]'
assert '[[ -n $SOME_VAR ]] (double quotes)' "[[ -n $SOME_VAR ]]"
assert '[[ -z $BLANK_VAR ]] (double quotes)' "[[ -z \"$BLANK_VAR\" ]]"

true
assert_ran_ok "assert_ran_ok on 'true'"

false
assert_not_ran_ok "assert_not_ran_ok on 'false'"

# Print results
report
