#!/bin/bash

# Load testing framework
. ./testlib.sh

# Test setup
. ./test_setup.sh

TEST_SUITE_NAME="Test sshd_config template creation"

# Number of tests
TOTAL_TESTS=3

$TEMPLATE_MAKER -p $OF_PREFIX-kv-1.txt -f $OF_PREFIX-1.in \
    -o $OF_PREFIX-1.out -a $OF_PREFIX-2.out
assert_ran_ok "Basic template creation ran ok"

assert "Template file output" "diff -u $OF_PREFIX-1.out $OF_PREFIX-1.cmp"
assert "Attributes file output" "diff -u $OF_PREFIX-2.out $OF_PREFIX-2.cmp"

# Print results
report
